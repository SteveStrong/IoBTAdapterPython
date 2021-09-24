import logging
import sys
from typing import Any
import time

import serial
from serial.threaded import LineReader, ReaderThread

#  https://pypi.org/project/signalrcore/
from signalrcore.hub_connection_builder import HubConnectionBuilder
from signalrcore.protocol.messagepack_protocol import MessagePackHubProtocol

#iobtBaseURL = "http://centralmodel"
#iobtBaseURL = "https://iobtweb.azurewebsites.net"
iobtBaseURL = "http://localhost:6010"


logger = logging.getLogger('LoraTransmit')
logger.setLevel(logging.DEBUG)  # set logger level
consoleHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(consoleHandler)


# https://www.crowdsupply.com/ronoth/lostik

class LoraTransmit(LineReader):

    def connection_made(self, transport):
        print("connection made")
        self.transport = transport
        self.send_cmd("sys set pindig GPIO11 0")
        self.send_cmd('sys get ver')
        self.send_cmd('radio get mod')
        self.send_cmd('radio get freq')
        self.send_cmd('radio get sf')
        self.send_cmd('mac pause')
        self.send_cmd('radio set pwr 10')
        self.send_cmd("sys set pindig GPIO11 0")
        self.frame_count = 0

    def handle_line(self, data):
        if data == "ok":
            return
        print("RECV: %s" % data)

    def connection_lost(self, exc):
        if exc:
            print(exc)
        print("port closed")

    def tx(self, message):
        self.send_cmd("sys set pindig GPIO11 1")
        message = message.encode('utf-8').hex()
        print(message)
        print(bytes.fromhex(message).decode('utf-8'))

        # txmsg = 'radio tx %x%x%s' % (int(time.time()), self.frame_count, message)
        txmsg = 'radio tx %s' % (message)
        print("Message : %s" % txmsg)
        self.send_cmd(txmsg)
        time.sleep(.3)
        self.send_cmd("sys set pindig GPIO11 0")
        self.frame_count = self.frame_count + 1

    def send_cmd(self, cmd, delay=.5):
        print("SEND: %s" % cmd)
        self.write_line(cmd)
        time.sleep(delay)


class SimpleClientHubConnector:
    azureURL: str
    hub_connection: Any = None

    def __init__(self, url: str) -> None:
        self.azureURL = url
        self.initialize()

    def initialize(self):
        hubUrl = f"{self.azureURL}/clientHub"
        if (self.hub_connection is not None):
            self.hub_connection.stop()

        # WARNING!!! signalr logging.DEBUG blocks execution of voice commands in voiceAssistant project.
        if (self.hub_connection is None):
            self.hub_connection = HubConnectionBuilder()\
                .with_url(hubUrl)\
                .configure_logging(logging.INFO)\
                .with_automatic_reconnect({
                    "type": "raw",
                    "keep_alive_interval": 60,
                    "reconnect_interval": 30,
                    "max_attempts": 5
                }).build()

            self.hub_connection.on_open(lambda: print(
                "connection opened and handshake received ready to send messages"))
            self.hub_connection.on_close(lambda: print("connection closed"))

    def start(self):
        try:
            self.hub_connection.start()
            time.sleep(1)
            self.hub_connection.on("Pong", self.receive_signalr_pong)

        except:
            print(f"client hub connector exception")
            raise

    def receive_signalr_pong(self, message):
        logger.debug(f"receive_signalr_pong={message}")
        print(f"receive_signalr_pong={message}")

        tx_port = "COM4"
        ser = serial.Serial(tx_port, baudrate=57600)
        with ReaderThread(ser, LoraTransmit) as protocol:
            protocol.tx(message)

    def stop(self):
        if (self.hub_connection):
            self.hub_connection.stop()

    def shutdown(self):
        if (self.hub_connection):
            self.hub_connection.stop()





def main():

    # seed random number generator

    print("Connecting to ", iobtBaseURL)
    iobtHub = SimpleClientHubConnector(iobtBaseURL)

    iobtHub.start()

    while(True):

        time.sleep(1)  # Sleep for 1 seconds


if __name__ == '__main__':
    main()

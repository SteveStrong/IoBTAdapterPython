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
iobtBaseURL = "http://localhost:6020"

logger = logging.getLogger('LoraReceive')
logger.setLevel(logging.DEBUG)  # set logger level
consoleHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(consoleHandler)

class SimpleClientHubConnector:
    azureURL: str
    hub_connection: Any = None

    def __init__(self, url: str) -> None:
        self.azureURL = url
        self.initialize()

    def initialize(self):
        hubUrl = f"{self.azureURL}/serverHub"
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
            self.hub_connection.on("Pong", self.receive_json)
            self.hub_connection.on("ActionStatus", self.receive_json)
            self.hub_connection.on("RX", self.receive_json)
            self.hub_connection.on("TX", self.receive_json)

        except:
            print(f"client hub connector exception")
            raise

    def receive_json(self, pong):
        print("")
        print(f"data={pong[0]}")

    def ping(self, msg: str):
        try:
            logger.debug(f"Send Ping msg={msg}")
            self.hub_connection.send('Ping', [msg])
        except:
            print(f"Error ${sys.exc_info()[0]}")
            return []

    def RX(self, rx: str):
        try:
            logger.debug(f"Send RX={rx}")
            self.hub_connection.send('RX', [rx])
        except:
            print(f"Error ${sys.exc_info()[0]}")
            return []

    def stop(self):
        if (self.hub_connection):
            self.hub_connection.stop()

    def shutdown(self):
        if (self.hub_connection):
            self.hub_connection.stop()



class MessagePublisher():
    iobtHub = None
    def init(self):
         if ( self.iobtHub is None):
            self.iobtHub = SimpleClientHubConnector(iobtBaseURL)
            self.iobtHub.start()
            print("hub is ready to receive from lora")
            self.iobtHub.ping("ready to recieve RX")

    def publish(self, message):
        if ( self.iobtHub is None):
            print("Must start signalr hub")
            return

        self.iobtHub.RX(message)


# https://www.crowdsupply.com/ronoth/lostik

class LoraReceive(LineReader):
    signalrClient = None 

    def connection_made(self, transport):
        print("connection made")
        self.transport = transport
        self.send_cmd('sys get ver')
        self.send_cmd('mac pause')
        self.send_cmd('radio set pwr 10')
        self.send_cmd('radio rx 0')
        self.send_cmd("sys set pindig GPIO10 0")
        if (self.signalrClient is None ):
            self.signalrClient = MessagePublisher()
            self.signalrClient.init()


    def handle_line(self, data):
        # print('handling line {0}'.format(data))
        if data == "ok" or data == 'busy':
            return
        if data == "radio_err":
            self.send_cmd('radio rx 0')
            return
        if 'RN2903' in data or '4294967245' in data:
            print('skipping line because data = {0}'.format(data))
            return

        self.send_cmd("sys set pindig GPIO10 1", delay=0)

        # Get Hex Data
        #print('getting message data with split " ", 1 [1]')
        message = data.split("  ", 1)[1]
        #print("Hex : %s" % message)

        # Convert to UTF-8
        message_txt = bytes.fromhex(message).decode('utf-8').strip()
        #print('sending {0} to signalrClient'.format(data))
        #print("Txt : %s" % message_txt)

        if (self.signalrClient is None ):
            self.signalrClient = MessagePublisher()
            self.signalrClient.init()

        self.signalrClient.publish(message_txt)

        time.sleep(.1)
        self.send_cmd("sys set pindig GPIO10 0", delay=1)
        self.send_cmd('radio rx 0')

    def connection_lost(self, exc):
        if exc:
            print(exc)
        print("closing port ")

    def send_cmd(self, cmd, delay=.01):
        self.transport.write(('%s\r\n' % cmd).encode('UTF-8'))
        time.sleep(delay)






def main():

    tx_port = "COM5"
    ser = serial.Serial(tx_port, baudrate=57600)
    with ReaderThread(ser, LoraReceive) as protocol:
        while(True):
            #time.sleep(1)  # Sleep for 1 seconds
            pass


if __name__ == '__main__':
    main()

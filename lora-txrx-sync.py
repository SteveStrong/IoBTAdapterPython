import logging
import sys
from typing import Any
import time

import serial
from serial.threaded import LineReader, ReaderThread

#  https://pypi.org/project/signalrcore/
from signalrcore.hub_connection_builder import HubConnectionBuilder
from signalrcore.protocol.messagepack_protocol import MessagePackHubProtocol


# sys set pindig GPIO10 1 (turns on blue LED)
# sys set pindig GPIO10 0 (turns off blue LED)
# sys set pindig GPIO11 1 (turns on red LED)
# sys set pindig GPIO11 0 (turns off red LED)

#iobtBaseURL = "http://centralmodel"
#iobtBaseURL = "https://iobtweb.azurewebsites.net"
tx_rx_port = "COM5"
baud_rate = 57600
iobtBaseURL = "http://localhost:6010"


logger = logging.getLogger('LoraTransmit')
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
            time.sleep(0.5)
            self.hub_connection.on("Pong", self.receive_pong)
            self.hub_connection.on("TX", self.receive_TX)

            self.hub_connection.on("Pong", self.receive_json)
            self.hub_connection.on("ActionStatus", self.receive_json)
            self.hub_connection.on("RX", self.receive_json)
            self.hub_connection.on("TX", self.receive_json)

        except:
            print(f"client hub connector exception")
            raise

    def receive_pong(self, pong):
        print("")
        print(f"pong={pong}")

    def receive_json(self, data):
        print("")
        print(f"data={data[0]}")

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


    def receive_TX(self, data):
        tx = data[0]
        print("")
        print(f"tx={tx}")


        self.ser = serial.Serial(tx_rx_port, baudrate=baud_rate)
        with ReaderThread(self.ser, LoraTransmit) as protocol:
            protocol.tx(tx)

        print(f"this was sent via radio?={tx}")

    def stop(self):
        if (self.hub_connection):
            self.hub_connection.stop()

    def shutdown(self):
        if (self.hub_connection):
            self.hub_connection.stop()


iobtHub = SimpleClientHubConnector(iobtBaseURL)
iobtHub.start()
print("hub is ready to receive from lora")
iobtHub.ping("ready to receive RX")

# https://www.crowdsupply.com/ronoth/lostik

class LoraTransmit(LineReader):

    def connection_made(self, transport):
        print("LoraTransmit connection made  Turn on RED Light")
        self.transport = transport

        self.send_cmd('sys get ver')
        self.send_cmd('radio get mod')
        self.send_cmd('radio get freq')
        self.send_cmd('radio get sf')
        self.send_cmd('mac pause')
        self.send_cmd('radio set pwr 10')

    def handle_line(self, data):
        if data == "ok":
            return
        print("RECV: %s" % data)

    def connection_lost(self, exc):
        if exc:
            print(exc)
        print("port closed")

    def tx(self, message):
        print("Inside tx..............................")
        self.send_cmd("sys set pindig GPIO10 0") # turn off blue
        self.send_cmd("sys set pindig GPIO11 1")  # turn on red
        print(F"MSG={message}")
        message = message.encode('utf-8').hex()
        print(F"MSG={message}")
        #print(bytes.fromhex(message).decode('utf-8'))

        txmsg = 'radio tx %s' % (message)
        self.send_cmd(txmsg)
        self.send_cmd("sys set pindig GPIO11 0") # turn off red
        self.send_cmd("sys set pindig GPIO10 1") # turn on blue

    def send_cmd(self, cmd, delay=.01):
        # print("SEND: %s" % cmd)
        self.write_line(cmd)
        time.sleep(delay)


class LoraReceive(LineReader):

    def connection_made(self, transport):
        self.transport = transport
        print("LoraReceive  connection made Turn on blue light we are listening")
        self.send_cmd("sys set pindig GPIO10 1")  #turn on blue
        self.send_cmd('sys get ver')
        self.send_cmd('mac pause')
        self.send_cmd('radio set pwr 10')
        self.send_cmd('radio rx 0')


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

        self.send_cmd("sys set pindig GPIO10 1") #turn on blue

        # Get Hex Data
        #print('getting message data with split " ", 1 [1]')
        message = data.split("  ", 1)[1]
        #print("Hex : %s" % message)

        # Convert to UTF-8
        message_txt = bytes.fromhex(message).decode('utf-8').strip()
        #print('sending {0} to signalrClient'.format(data))
        #print("Txt : %s" % message_txt)


        #push data into the squire
        iobtHub.RX(message_txt)

        # time.sleep(.1)
        # self.send_cmd("sys set pindig GPIO10 1") #turn on blue
        self.send_cmd('radio rx 0')

    def connection_lost(self, exc):
        if exc:
            print(exc)
        print("closing port ")

    def send_cmd(self, cmd, delay=.01):
        self.transport.write(('%s\r\n' % cmd).encode('UTF-8'))
        time.sleep(delay)



def main():

    print("Connecting to ", iobtBaseURL)

    ser = serial.Serial(tx_rx_port, baudrate=baud_rate)
    with ReaderThread(ser, LoraReceive) as protocol:
        while(True):
            #time.sleep(1)  # Sleep for 1 seconds
            pass


if __name__ == '__main__':
    main()

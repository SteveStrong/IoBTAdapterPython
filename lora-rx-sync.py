import logging
import json
import sys
from typing import Any
import time


import serial
from serial.threaded import LineReader, ReaderThread

#  https://pypi.org/project/signalrcore/
from signalrcore.hub_connection_builder import HubConnectionBuilder
from signalrcore.protocol.messagepack_protocol import MessagePackHubProtocol



def LoraTXRX(port, iobtBaseURL:str):

    logger = logging.getLogger('LoraReceive')
    logger.setLevel(logging.DEBUG)  # set logger level
    consoleHandler = logging.StreamHandler(sys.stdout)
    logger.addHandler(consoleHandler)

    class SimpleClientHubConnector:
        squireURL: str
        hub_connection: Any = None

        def __init__(self, url: str) -> None:
            self.squireURL = url
            self.initialize()

        def initialize(self):
            hubUrl = f"{self.squireURL}/serverHub"
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

                self.hub_connection.on_open(lambda: print("connection opened and handshake received"))
                self.hub_connection.on_close(lambda: print("connection closed"))

        def start(self):
            try:
                self.hub_connection.start()
                time.sleep(1)
                self.hub_connection.on("Pong", self.receive_PONGjson)
                self.hub_connection.on("ActionStatus", self.receive_ASjson)
                self.hub_connection.on("RX", self.receive_RXjson)
                self.hub_connection.on("TX", self.receive_TXjson)

            except:
                print(f"client hub connector exception")
                raise

        def receive_PONGjson(self, pong):
            print("")
            print(f"pong={pong[0]}")

        def receive_ASjson(self, data):
            print("ActionStatus: receive_ASjson....")
            print(json.dumps(data, indent=3, sort_keys=True))

        def receive_RXjson(self, data):
            print("RX: receive_RXjson....")
            print(json.dumps(data, indent=3, sort_keys=True))

        def receive_TXjson(self, data):
            print("TX: receive_TXjson....")
            print(json.dumps(data, indent=3, sort_keys=True))

        def ping(self, msg: str):
            try:
                logger.debug(f"Send Ping msg={msg}")
                self.hub_connection.send('Ping', [msg])
            except:
                print(f"Error ${sys.exc_info()[0]}")
                return []

        def RX(self, rx: str):
            try:
                logger.debug(f"Sending to server RX={rx}")
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


    iobtHub = SimpleClientHubConnector(iobtBaseURL)
    iobtHub.start()

     

    # https://www.crowdsupply.com/ronoth/lostik

    class LoraReceive(LineReader):

        def connection_made(self, transport):
            print("-------------------------------")
            print("connection made")
            self.transport = transport
            self.send_cmd('sys get ver')
            self.send_cmd('mac pause')
            self.send_cmd('radio set pwr 10')
            self.send_cmd('radio rx 0')
            self.send_cmd("sys set pindig GPIO10 0")

        def turn_on_blue_light(self):
            # print("'''''''''''''''''''''''''''''''''")
            self.send_cmd("sys set pindig GPIO10 1") #turn on blue

        def turn_off_blue_light(self):
            self.send_cmd("sys set pindig GPIO10 0") #turn off blue


        def handle_line(self, data):
            if data == "ok" or data == 'busy':
                return
            if data == "radio_err":
                self.send_cmd('radio rx 0')
                return
            if 'RN2903' in data or '4294967245' in data:
                print(F'skipping line because data = {data}')
                return

            print(F'LoraReceive: handling line {data}')
            #self.send_cmd("sys set pindig GPIO10 1", delay=0)

            # Get Hex Data
            #print('getting message data with split " ", 1 [1]')
            message = data.split("  ", 1)[1]
            #print("Hex : %s" % message)

            # Convert to UTF-8
            message_txt = bytes.fromhex(message).decode('utf-8').strip()
            iobtHub.RX(message_txt)
            self.send_cmd('radio rx 0')

        def connection_lost(self, exc):
            if exc:
                print(exc)
            print("port closed")
            print("-------------------------------")

        def send_cmd(self, cmd, delay=.01):
            self.transport.write(('%s\r\n' % cmd).encode('UTF-8'))
            time.sleep(delay)

    open_port = serial.Serial(port, baudrate=57600)
    with ReaderThread(open_port, LoraReceive) as protocol:
        protocol.turn_on_blue_light()
        while(True):
            time.sleep(.01) 

            



def main():


    #iobtBaseURL = "http://centralmodel"
    #iobtBaseURL = "https://iobtweb.azurewebsites.net"
    iobtBaseURL = "http://localhost:7020"

    LoraTXRX("COM9",iobtBaseURL)

   


if __name__ == '__main__':
    main()

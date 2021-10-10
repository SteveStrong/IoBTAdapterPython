import logging
import json
import sys
from typing import Any
import time

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


def main():


    #iobtBaseURL = "http://centralmodel"
    iobtBaseURL = "https://iobtweb.azurewebsites.net"


    LoraTXRX("COM9",iobtBaseURL)

  


if __name__ == '__main__':
    main()

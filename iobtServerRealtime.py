import logging
import sys
from typing import Any
import time

from signalrcore.hub_connection_builder import HubConnectionBuilder
from .models.udto_message import UDTO_Command, UDTO_Position, UDTO_ChatMessage

logger = logging.getLogger('iobtServerRealtime')
logger.setLevel(logging.DEBUG)  # set logger level
consoleHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(consoleHandler)


class IoBTClientHubConnector:
    azureURL: str
    hub_connection: Any = None

    def __init__(self, url: str) -> None:
        self.azureURL = url
        self.initialize()

    def initialize(self):
        hubUrl = f"{self.azureURL}/clientHub"
        if (self.hub_connection is not None):
            self.hub_connection.stop()

        if (self.hub_connection is None):
            self.hub_connection = HubConnectionBuilder()\
                .with_url(hubUrl)\
                .configure_logging(logging.WARNING)\
                .with_automatic_reconnect({
                    "type": "raw",
                    "keep_alive_interval": 60,
                    "reconnect_interval": 30,
                    "max_attempts": 5
                }).build()

            # self.hub_connection.on("ChatMessage", self.handle_receive_message)

    def start(self):
        try:
            self.hub_connection.start()
            time.sleep(1)
            self.hub_connection.on("Pong", self.print_pong)
            self.hub_connection.on("Position", self.print_position)
        except:
            print(f"client hub connector exception")
            raise

        # callback()

    def print_pong(self, payload):
        logger.debug(f"print_pong payload={payload}")
        print(f"print_pong payload={payload}")

    def print_position(self, payload):
        # logger.debug(f"print_position payload={payload}")
        print(f"print_position payload={payload}")

    def chatMessage(self, obj: UDTO_ChatMessage):
        try:
            logger.debug(f"chatMessage obj={obj.message}")
            self.hub_connection.send(obj.udtoTopic, [obj])
        except:
            print(f"Error ${sys.exc_info()[0]}")
            return []

    def command(self, obj: UDTO_Command):
        try:
            logger.debug(f"command obj={obj.message}")
            self.hub_connection.send(obj.udtoTopic, [obj])
        except:
            print(f"Error ${sys.exc_info()[0]}")
            return []

    def position(self, obj: UDTO_Position):
        try:
            #logger.debug(f"command obj={obj.message}")
            self.hub_connection.send(obj.udtoTopic, [obj])
        except:
            print(f"Error ${sys.exc_info()[0]}")
            return []

    def handle_receive_message(self, payload):
        print(f"receive_message payload={payload}")

    def handle_receive_ping(self, payload):
        print(f"receive ping payload={payload}")

    def stop(self):
        if (self.hub_connection):
            self.hub_connection.stop()

    def shutdown(self):
        if (self.hub_connection):
            self.hub_connection.stop()

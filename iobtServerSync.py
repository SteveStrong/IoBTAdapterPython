import logging
import sys
from typing import Any
import time

from signalrcore.hub_connection_builder import HubConnectionBuilder
from .models.udto_message import UDTO_Command, UDTO_Position, UDTO_ChatMessage

logger = logging.getLogger('IoBTServerHubConnector')
logger.setLevel(logging.DEBUG)  # set logger level
consoleHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(consoleHandler)


class IoBTServerHubConnector:
    azureURL: str
    hub_connection: Any = None

    def __init__(self, url: str) -> None:
        self.azureURL = url
        self.initialize()

    def initialize(self):
        hubUrl = f"{self.azureURL}/serverHub"
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

    def start(self, hooks):
        try:
            self.hub_connection.start()
            time.sleep(1)
            self.hub_connection.on("Ping", hooks.on_ping)
            self.hub_connection.on("Position", hooks.on_position)
            self.hub_connection.on("Send", hooks.on_send)
            self.hub_connection.on("Monitor", hooks.on_monitor)
        except:
            print(f"client hub connector exception")
            raise


    def ping(self, msg: str):
        try:
            logger.debug(f"Send Ping msg={msg}")
            self.hub_connection.send('Ping', [msg])
        except:
            print(f"Error ${sys.exc_info()[0]}")
            return []

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
            print(f"send position payload={obj}")
            self.hub_connection.send(obj.udtoTopic, [obj])
        except:
            print(f"Error ${sys.exc_info()[0]}")
            return []

    def stop(self):
        if (self.hub_connection):
            self.hub_connection.stop()


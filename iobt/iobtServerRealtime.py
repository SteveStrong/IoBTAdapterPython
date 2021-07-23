import logging

from signalrcore.hub_connection_builder import HubConnectionBuilder


from .models.udto_message import UDTO_Position, UDTO_ChatMessage

class ClientHubConnector:
    azureURL:str


    def __init__(self, url:str) -> None:
        self.azureURL = url
        self.initialize()

    def initialize(self):
        hubUrl = f"{self.azureURL}/clientHub"
        if (self.hub_connection is not None):
            self.hub_connection.stop()

        if (self.hub_connection is None):
            self.hub_connection = HubConnectionBuilder()\
                .with_url(hubUrl)\
                    .configure_logging(logging.DEBUG)\
                    .with_automatic_reconnect({
                    "type": "raw",
                    "keep_alive_interval": 60,
                    "reconnect_interval": 30,
                    "max_attempts": 5
                }).build()

            self.hub_connection.on("ChatMessage", self.handle_receive_message)

        self.hub_connection.start()  

    def handle_receive_message(self, payload):
        print(f"receive_message payload={payload}")

    def stop(self):
        if (self.hub_connection):
            self.hub_connection.stop()

    def shutdown(self):
        if (self.hub_connection):
            self.hub_connection.stop()      

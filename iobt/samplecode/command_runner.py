import logging
import typing
from iobt.models.udto_message import UDTO_Base, UDTO_ChatMessage, UDTO_Command
import requests

from signalrcore.hub_connection_builder import HubConnectionBuilder

_LOGGER = logging.getLogger("iobt.command-runner")

class CommandRunner:
    message_text: str = ''
    hub_connection: typing.Any = None
    test_udto_init = dict({
            "user": "Llam_9",
            "message": "default message",
            "sourceGuid": "375ad623-6e7c-4272-8aa7-d631d22a356d",
            "timeStamp": "2021-04-07T11:55:46.669Z",
            "personId": "Llam_9"
          })
    udto_message: UDTO_ChatMessage
    base_url = "https://iobtweb.azurewebsites.net"

    def __init__(self) -> None:
        self.initialize()

    def initialize(self):
        chatHubUrl = f"{self.base_url}/clientHub"
        if (self.hub_connection is not None):
            self.hub_connection.stop()

        if (self.hub_connection is None):
            self.hub_connection = HubConnectionBuilder()\
                .with_url(chatHubUrl)\
                    .configure_logging(logging.DEBUG)\
                    .with_automatic_reconnect({
                    "type": "raw",
                    "keep_alive_interval": 60,
                    "reconnect_interval": 30,
                    "max_attempts": 5
                }).build()
            self.hub_connection.on("ChatMessage", self.handle_receive_message)

        self.hub_connection.start()

    def send_zoom_in(self):
        print(f"in send_zoom_in")
        udto_command = UDTO_Command(self.test_udto_init)
        udto_command.targetGuid = self.test_udto_init['sourceGuid']
        udto_command.command = 'ZOOM_IN'
        udto_command.args = []
        self.hub_connection.send("Command", [udto_command])

    def send_zoom_out(self):
        print(f"in send_zoom_out")
        udto_command = UDTO_Command(self.test_udto_init)
        udto_command.targetGuid = self.test_udto_init['sourceGuid']
        udto_command.command = 'ZOOM_OUT'
        udto_command.args = []
        self.hub_connection.send("Command", [udto_command])

    def send_hide_map(self):
        print(f"in hide map")
        udto_command = UDTO_Command(self.test_udto_init)
        udto_command.targetGuid = self.test_udto_init['sourceGuid']
        udto_command.command = 'HIDE_MAP'
        udto_command.args = []
        self.hub_connection.send("Command", [udto_command])

    def send_show_map(self):
        print(f"in show map")
        udto_command = UDTO_Command(self.test_udto_init)
        udto_command.targetGuid = self.test_udto_init['sourceGuid']
        udto_command.command = 'SHOW_MAP'
        udto_command.args = []
        self.hub_connection.send("Command", [udto_command])

    def send_chat_message(self, message_text: str):
        print(f"in send_chat with message_text={message_text}")
        self.message_text = message_text
        # self.post_message(text)
        # self.post_message()
        udto_message = UDTO_ChatMessage(self.test_udto_init)
        udto_message.message = self.message_text
        self.hub_connection.send("ChatMessage", [udto_message])

    # testing with REST in case signalr isn't working
    def post_message(self):
        udto_message = UDTO_ChatMessage(self.test_udto_init)
        udto_message.message = self.message_text
        # message = self.test_message
        # message['message'] = self.message_text
        chatURL = f"{self.base_url}/api/ClientHub/ChatMessage"
        headers = dict({'Content-type':'application/json', 'Accept':'application/json'})
        print(f"Before toJSON")
        print(f"message json={udto_message.toJSON()}")
        print(f"After toJSON")
        response = requests.post(url = chatURL, data = udto_message.toJSON(), headers = headers)
        # response = requests.post(url = chatURL, json = dict(udto_message.toJSON()), headers = headers)
        result = response.json()
        #print(result)
        if ( result['hasError'] == True):
            print(result['hasError is True message'])
        else:
            payload = result['payload']
            print(f"post_message payload={payload}")

    def handle_receive_message(self, payload):
        print(f"receive_message payload={payload}")

    def stop(self):
        if (self.hub_connection):
            self.hub_connection.stop()

    def shutdown(self):
        if (self.hub_connection):
            self.hub_connection.stop()



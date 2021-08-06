from datetime import datetime
from models.udto_message import UDTO_ChatMessage
import json
import os
import sys
import time
import requests
import logging
import uuid
import paho.mqtt.client as mqtt

# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger("main")  # Logger for this module
logger.setLevel(logging.INFO)  # Debugging for this file.
# Initialize Logging

# Define some stuff
# BROKER_HOST = "localhost"

KEEPALIVE = 60
BROKER_HOST = "demo.iobtlab.com"
BROKER_PORT = 1883
CLIENT_ID = "me"  # what do we want to use?
client = None  # MQTT client instance. See init_mqtt()


# this should puhlish what is found to RxPY
# https://github.com/ReactiveX/RxPY

class MQTTListenerForUDTO:

    def __init__(self):
        self.client = mqtt.Client(client_id=CLIENT_ID, clean_session=False)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        self.message_count = 0

        # Our MQTT Client. See PAHO documentation for all configurable options.
        # "clean_session=True" means we don"t want Broker to retain QoS 1 and 2 messages
        # for us when we"re offline. You"ll see the "{"session present": 0}" logged when
        # connected.

        # Route Paho logging to Python logging.
        self.client.enable_logger()

        # Setup callbacks

    def sendUDTO(self, topic, data):
        if topic == "UDTO_ChatMessage":
            payload = UDTO_ChatMessage(data)
            self.client.publish(topic, payload)

    def setCallback(self, call_me):
        self.call_me = call_me

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def start(self):
        # Connect to Broker.
        self.client.connect(BROKER_HOST, BROKER_PORT)
        # self.client.connect_async(BROKER_HOST, BROKER_PORT, KEEPALIVE)

    def do_loop(self):
        self.client.loop_start()

    """
    MQTT Related Functions and Callbacks
    """

    def on_connect(self, client, user_data, flags, connection_result_code):
        """on_connect is called when our program connects to the MQTT Broker.
        Always subscribe to topics in an on_connect() callback.
        This way if a connection is lost, the automatic
        re-connection will also results in the re-subscription occurring."""

        if connection_result_code == 0:
            # 0 = successful connection
            logger.info("Connected to MQTT Broker")
        else:
            # connack_string() gives us a user friendly string for a connection code.
            logger.error("Failed to connect to MQTT Broker: " +
                         mqtt.connack_string(connection_result_code))

        # Subscribe to the topic
        client.subscribe('UDTO_ChatMessage', qos=2)

    def on_disconnect(self, client, user_data, disconnection_result_code):
        """Called disconnects from MQTT Broker."""
        logger.error("Disconnected from MQTT Broker")

    def on_message(self, client, userdata, msg):
        """Callback called when a message is received on a subscribed topic."""
        data = None

        topic = msg.topic
        timestamp = msg.timestamp
        if topic == "UDTO_ChatMessage":
            payload = UDTO_ChatMessage(data)
            payload.timeStamp = msg.timestamp

        try:
            self.call_me(msg)
            data = json.loads(msg.payload.decode("UTF-8"))
        except json.JSONDecodeError as e:
            print("JSON Decode Error: " + msg.payload.decode("UTF-8"))

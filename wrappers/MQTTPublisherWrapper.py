from datetime import datetime
from ..iobtServerRealtime import IoBTClientHubConnector
from typing import Any
from ..models.udto_message import UDTO_ChatMessage, UDTO_Command, UDTO_Position
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
# BROKER_HOST = "demo.iobtlab.com"
# BROKER_PORT = 1883
CLIENT_ID = "MQTTPublish" 
client = None  # MQTT client instance. See init_mqtt()


class MQTTPublisherWrapper:

    def __init__(self, broker_host: str, broker_port: int):

        self.broker_host = broker_host
        self.broker_port = broker_port

        self.client = mqtt.Client(client_id=CLIENT_ID, clean_session=False)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.client.enable_logger()


    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def start(self):
        # Connect to Broker.
        self.client.connect(self.broker_host, self.broker_port)

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

    def on_disconnect(self, client, user_data, disconnection_result_code):
        """Called disconnects from MQTT Broker."""
        logger.error("Disconnected from MQTT Broker")


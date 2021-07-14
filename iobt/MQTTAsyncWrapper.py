import json
import os
import sys
import time
import logging

import paho.mqtt.client as mqtt


class MQTTAsyncWrapper:
    sourceIP:str

    def __init__(self, name, sourceIP):
        self.sourceIP = sourceIP
        self.client = mqtt.Client(name)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        self.message_count = 0

    def start_MQTT(self):
        KEEPALIVE = 60
        if self.sourceIP is None:
            print("No MQTT sourceIP specified")
            return

        # https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php

        host, port = self.sourceIP.split(":")
        url = F"http://{host}"
        print(F"paho: connecting to {url}:{port}")
        self.client.connect_async(url, int(port), KEEPALIVE)
        # self.client.connect( host, int( port ), KEEPALIVE )
        self.client.loop_start()  #starts

    def stop_MQTT(self):
        self.client.loop_stop()
        self.client.disconnect()

    def sendCommand(self, command, content=None, topic=None):
    
        message = {"command": command, "origin": "PC", "content": content}

        item = json.dumps(message)
        self.client.publish(topic, payload=item)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.message_count = 0
            client.connected_flag = True  # set flag
            print("Connected OK,  start subscribe")
        
            message = {"command": "it works kinda", "origin": "Steve"}
            print(message)

            item = json.dumps(message)
            self.client.publish("simple33", payload=item)

        else:
            print("Bad connection, RC = ", rc)
            mqtt.Client.bad_connection_flag = True

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")

    def on_message(self, client, userdata, msg):
        print(msg)
        topic = msg.topic
        timestamp = msg.timestamp
        #delta = timestamp - self.last_timestamp
        # if delta <= 0.00001:
        #     print(F"same message {msg.timestamp}")
        #     return

        print(F"{topic} same message {msg} {timestamp}")

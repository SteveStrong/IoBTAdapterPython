from datetime import datetime
import json
import os
import sys
import time
import requests
import logging
import uuid

from iobt.models.udto_message import UDTO_Position, UDTO_ChatMessage
from iobt.iobtServerRest import IobtServerRest
#from iobt.iobtServerRealtime import ClientHubConnector
from iobt.MQTTWrapper import MQTTWrapper

                                        

#  https://iobtweb.azurewebsites.net/swagger/index.html



# def signal_handler(sig, frame):
#     """Capture Control+C and disconnect from Broker."""

#     logger.info("You pressed Control + C. Shutting down, please wait...")

#     client.disconnect() # Graceful disconnection.

#     sys.exit(0)



                                                 







if __name__ == '__main__':

    
    #iobtURL = "http://localhost:5000"
    iobtURL = "https://iobtweb.azurewebsites.net"


    # mqttHUB.topics({
    #     'UDTO_ChatMessage': doMessage, 
    # })


    iobtRest = IobtServerRest(iobtURL)

    def doMessage(msg):     
        try:   
            print("mesage sent to Iobt server")
            topic = msg.topic
            data = json.loads(msg.payload.decode("UTF-8"))    
            timestamp = msg.timestamp
            print(data)
            iobtRest.chatMessage(UDTO_ChatMessage(data))
 
            payload = iobtRest.currentChatMessage()
            print(payload)

            print(F"Received message for topic {topic} {timestamp}: {payload}")
        except:
            print("Unhandled message topic {} with payload " + str(msg.topic, msg.payload))
        



    mqttHUB = MQTTWrapper();
    mqttHUB.setCallback(doMessage)

    mqttHUB.start()

    iobtRest.flushCentralModel()
    #payload = iobtRest.centralModel()
    #print(payload)

    udto_message = UDTO_ChatMessage({
        "user": "Llam_15",
        "message": "new xxxxworking a Message",
        })


    # mqtt publish 
    mqttHUB.publish('UDTO_ChatMessage',udto_message.toJSONString())

    #payload = iobtRest.chatMessage(udto_message)
    #print(payload)

    ##payload = iobtRest.currentChatMessage()
    ##print(payload)

    mqttHUB.doLoop()

 
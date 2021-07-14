##  =========================================
 
import os
from gps import *
from time import *
import time
import threading
import json
import requests
import paho.mqtt.client as mqtt


##  http://demo.iobtlab.com:1883/



# Vars =======================
url = "https://localhost:8080/location/current"
mqtt_topic = "/squire-202"
mqtt_ip_address="10.8.0.17"
mqtt_port=1883
mqtt_timeout=60
# ============================

gpsd = None #setting the global variable

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  gpsp.start() # start it up

  while True:
    try:
      payload = {'lat': gpsd.fix.latitude, 'lon':gpsd.fix.longitude, 'mode':gpsd.fix.mode,
                     'sats':0, 'sats_valid':0,
                     'speed':0,
                     'alt':gpsd.fix.altitude, 'climb':gpsd.fix.climb, 'track':gpsd.fix.track, 'time':"2019-12-30T18:35:02.000Z"}


      print(json.dumps(payload))
      r = requests.post(url, json=payload, verify=False)
      print(r.status_code, r.reason)

      # Publish to MQTT
      client = mqtt.Client()
      client.connect(mqtt_ip_address, mqtt_port, mqtt_timeout)
      client.publish(mqtt_topic, json.dumps(payload));
      client.disconnect();

      time.sleep(15)
    except requests.exceptions.RequestException as e:
      print(e)
      time.sleep(60)
    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
      print("\nKilling Thread...")
      exit(1)

      gpsp.running = False
      gpsp.join() # wait for the thread to finish what it's doing

  print ("Done.\nExiting.")

#!/usr/bin/env python3

import time
import sys
import serial
import argparse 
import re
# import message_receiver as mqtt
from serial.threaded import LineReader, ReaderThread
import paho.mqtt.client as mqtt

# Vars =======================
mqtt_topic = "iobt/udto/position"
mqtt_ip_address="127.0.0.1"
mqtt_port=1883
mqtt_timeout=60
# ============================

class MessagePublisher():

    def publish(self, message):
        client = mqtt.Client()
        client.connect(mqtt_ip_address, mqtt_port, mqtt_timeout)
        client.publish(mqtt_topic, message)
        client.disconnect()

class PrintLines(LineReader):

    def connection_made(self, transport):
        print("connection made")
        self.transport = transport
        print('send cmd: sys get ver')
        self.send_cmd('sys get ver')
        print('send cmd: mac pause')
        self.send_cmd('mac pause')
        print('send cmd: radio set pwr 10')
        self.send_cmd('radio set pwr 10')
        print('send cmd: radio rx 0')
        self.send_cmd('radio rx 0')
        print('send cmd: sys set pindig GPIO10 0')
        self.send_cmd("sys set pindig GPIO10 0")

    def handle_line(self, data):
        print('handling line {0}'.format(data))
        if data == "ok" or data == 'busy':
            return
        if data == "radio_err":
            self.send_cmd('radio rx 0')
            return
        if 'RN2903' in data or '4294967245' in data:
            print('skipping line because data = {0}'.format(data))
            return

        print('send cmd: sys set pindig GPIO10 1')
        self.send_cmd("sys set pindig GPIO10 1", delay=0)

        # Get Hex Data
        print('getting message data with split " ", 1 [1]')
        message = data.split("  ", 1)[1]
        print("Hex : %s" % message)

        # Convert to UTF-8
        print("Converting to UTF=8")
        message_txt=bytes.fromhex(message).decode('utf-8').strip()
        print("Txt : %s" % message_txt)

        # Send to MQTT
        print('sending {0} to MQTT'.format(message_txt))
        mqttClient = MessagePublisher()
        mqttClient.publish(message_txt)


        time.sleep(.1)
        print('send cmd: sys set pindig GPIO10 0')
        self.send_cmd("sys set pindig GPIO10 0", delay=1)
        print('send cmd: radio rx 0')        
        self.send_cmd('radio rx 0')

    def connection_lost(self, exc):
        if exc:
            print(exc)
        print("closing port result from'connect_lost(self,exc)")

    def send_cmd(self, cmd, delay=.5):
        print('send_cmd(self,cmd,delay=5 with percent sbackslashRbackslashM percent cmd encoding UTF-8')
        self.transport.write(('%s\r\n' % cmd).encode('UTF-8'))
        time.sleep(delay)


# Main ============================

# parser = argparse.ArgumentParser(description='LoRa Radio mode receiver.')
# parser.add_argument('port', help="Serial port descriptor")
# args = parser.parse_args()

# ser = serial.Serial(args.port, baudrate=57600)
ser = serial.Serial("/dev/ttyUSB0", baudrate=57600)
with ReaderThread(ser, PrintLines) as protocol:
    while(1):
        pass
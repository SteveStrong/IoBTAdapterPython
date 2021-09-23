#!/usr/bin/env python3

import time
import sys
import serial
import argparse
from serial.threaded import LineReader, ReaderThread

import paho.mqtt.client as mqtt
import radio_sender as radio

# Vars =======================
mqtt_topic="iobt/lora/tx"
mqtt_ip_address="127.0.0.1"
mqtt_port=1883
mqtt_timeout=60
radio_port="/dev/ttyUSB0"
# ============================

class PrintLines(LineReader):

    def connection_made(self, transport):
        print("connection made")
        self.transport = transport
        self.send_cmd("sys set pindig GPIO11 0")
        self.send_cmd('sys get ver')
        self.send_cmd('radio get mod')
        self.send_cmd('radio get freq')
        self.send_cmd('radio get sf')
        self.send_cmd('mac pause')
        self.send_cmd('radio set pwr 10')
        self.send_cmd("sys set pindig GPIO11 0")
        self.frame_count = 0

    def handle_line(self, data):
        if data == "ok":
            return
        print("RECV: %s" % data)

    def connection_lost(self, exc):
        if exc:
            print(exc)
        print("port closed")

    def tx(self, message):
        self.send_cmd("sys set pindig GPIO11 1")
        message = message.encode('utf-8').hex()
        print(message)
        print(bytes.fromhex(message).decode('utf-8'))

        # txmsg = 'radio tx %x%x%s' % (int(time.time()), self.frame_count, message)
        txmsg = 'radio tx %s' % (message)
        print("Message : %s" % txmsg)
        self.send_cmd(txmsg)
        time.sleep(.3)
        self.send_cmd("sys set pindig GPIO11 0")
        self.frame_count = self.frame_count + 1

    def send_cmd(self, cmd, delay=.5):
        print("SEND: %s" % cmd)
        self.write_line(cmd)
        time.sleep(delay)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_topic)


def on_message(client, userdata, msg):
    ser = serial.Serial(radio_port, baudrate=57600)
    message = msg.payload.decode()
    print(message)
    with ReaderThread(ser, radio.PrintLines) as protocol:
        protocol.tx(message)


# Main ============================
client = mqtt.Client()
client.connect(mqtt_ip_address, mqtt_port, mqtt_timeout)
# client.disconnect()

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()

#parser = argparse.ArgumentParser(description='LoRa Radio mode sender.')
#parser.add_argument('port', help="Serial port descriptor")
#args = parser.parse_args()


# ser = serial.Serial("/dev/ttyUSB0", baudrate=57600)
# with ReaderThread(ser, PrintLines) as protocol:
#     while(1):
#         protocol.tx()
#         time.sleep(10)


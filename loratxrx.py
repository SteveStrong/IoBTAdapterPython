import logging
import queue
import json
import sys
from typing import Any
import time
from numpy import number

import serial
from serial.threaded import LineReader, ReaderThread

#  https://pypi.org/project/signalrcore/
from signalrcore.hub_connection_builder import HubConnectionBuilder
from signalrcore.protocol.messagepack_protocol import MessagePackHubProtocol


# sys set pindig GPIO10 1 (turns on blue LED)
# sys set pindig GPIO10 0 (turns off blue LED)
# sys set pindig GPIO11 1 (turns on red LED)
# sys set pindig GPIO11 0 (turns off red LED)

#iobtBaseURL = "http://centralmodel"
#iobtBaseURL = "https://iobtweb.azurewebsites.net"

def LoraTXRX(panid, port, iobtBaseURL: str):

    logger = logging.getLogger('LoraTxRx')
    logger.setLevel(logging.DEBUG)  # set logger level
    consoleHandler = logging.StreamHandler(sys.stdout)
    logger.addHandler(consoleHandler)

    itemsToSend = queue.Queue()

    def sendQueuedItems():
        items_sent = 0
        yield F"items sent => {items_sent}"
        while True:
            if (not itemsToSend.empty()):
                item = itemsToSend.get()
                yield "Q Ready => " + item.tx
                item.send()
                yield "Q Sent=> " + item.tx
                time.sleep(2)
                items_sent += 1
                yield F"items sent => {items_sent}"


    def sendItemsUntilEmpty():
        items_sent = 0
        empty = itemsToSend.empty()
        while not empty:
            item = itemsToSend.get()
            item.send()
            items_sent += 1
            yield F"{items_sent} Sent=> " + item.tx
            time.sleep(.01)
            empty = itemsToSend.empty()
        return



    class SimpleClientHubConnector:
        squireURL: str
        hub_connection: Any = None

        def __init__(self, url: str) -> None:
            self.squireURL = url
            self.initialize()

        def initialize(self):
            hubUrl = f"{self.squireURL}/serverHub"
            if (self.hub_connection is not None):
                self.hub_connection.stop()

            # WARNING!!! signalr logging.DEBUG blocks execution of voice commands in voiceAssistant project.
            if (self.hub_connection is None):
                self.hub_connection = HubConnectionBuilder()\
                    .with_url(hubUrl)\
                    .configure_logging(logging.INFO)\
                    .with_automatic_reconnect({
                        "type": "raw",
                        "keep_alive_interval": 60,
                        "reconnect_interval": 30,
                        "max_attempts": 5
                    }).build()

                self.hub_connection.on_open(lambda: print(
                    "connection opened signalr is ready"))
                self.hub_connection.on_close(
                    lambda: print("signalr connection closed"))

        def start(self):
            try:
                self.hub_connection.start()
                time.sleep(0.2)
                self.hub_connection.on("Pong", self.receive_PONGjson)
                self.hub_connection.on(
                    "ReassignPanID", self.receive_REASSIGNjson)
                self.hub_connection.on("ActionStatus", self.receive_ASjson)
                self.hub_connection.on("Share", self.receive_SHAREjson)
                self.hub_connection.on("RX", self.receive_RXjson)
                self.hub_connection.on("TX", self.receive_TXjson)

                self.hub_connection.send('ReassignPanID', [panid])
                print(f"event listeners connected")

            except:
                print(f"client hub connector exception")
                raise

        def receive_PONGjson(self, pong):
            print("")
            print(f"pong={pong[0]}")

        def receive_SHAREjson(self, data):
            print("Share: receive_SHAREjson....")
            print(json.dumps(data, indent=3, sort_keys=True))

        def receive_REASSIGNjson(self, data):
            print("ReassignPanID: receive_REASSIGNjson....")
            print(json.dumps(data, indent=3, sort_keys=True))

        def receive_ASjson(self, data):
            print("ActionStatus: receive_ASjson....")
            print(json.dumps(data, indent=3, sort_keys=True))

        def receive_RXjson(self, data):
            print("RX: receive_RXjson....")
            print(json.dumps(data, indent=3, sort_keys=True))

        def receive_TXjson(self, data):
            print("TX: receive_TXjson....")
            print(json.dumps(data, indent=3, sort_keys=True))

            # send this to radio
            # new messages will restart this port, you must wait until is closes
            # so you better queue the messages and feed them out when you are ready
            try:
                item = TXSender(port, data[0])
                itemsToSend.put(item)
                print(F"item pushed ${item.tx}")
            except:
                print(f"receive_TX exception")

        def ping(self, msg: str):
            try:
                #logger.debug(f"Send Ping msg={msg}")
                self.hub_connection.send('Ping', [msg])
            except:
                print(f"Error ${sys.exc_info()[0]}")
                return []

        def RX(self, rx: str):
            try:
                logger.debug(f"Sending to server RX={rx}")
                self.hub_connection.send('RX', [rx])
            except:
                print(f"Error {sys.exc_info()[0]}")
                return []

        def receive_TX(self, data):
            print("TX: receive_TX....")
            print(json.dumps(data, indent=3, sort_keys=True))

            # new messages will restart this port, you must wait until is closes
            # so you better queue the messages and feed them out when you are ready
            try:
                item = TXSender(port, data[0])
                itemsToSend.put(item)
                print(F"item pushed {item.tx}")
            except:
                print(f"receive_TX exception")

        def radio_loop_TX(self):
            self.ping(F"Lora radio is transmitting {port}")
            print(F"radio_loop_TX {port}")
            gen = sendQueuedItems()
            while(True):
                result = next(gen)
                print(result)

        def radio_loop_RX(self):
            self.ping(F"Lora radio is listening {port}")
            print(F"radio_loop_RX {port}")
            open_port = serial.Serial(port, baudrate=57600)
            with ReaderThread(open_port, LoraReceive) as protocol:
                protocol.turn_on_blue_light()
                while(True):
                    time.sleep(.01)

        def run(self):
            self.ping(F"Lora radio is running on {port}")
            while(itemsToSend.empty()):
                open_port = serial.Serial(port, baudrate=57600)
                with ReaderThread(open_port, LoraReceive) as protocol:
                    protocol.turn_on_blue_light()
                    while(itemsToSend.empty()):
                        time.sleep(.01)

                gen = sendItemsUntilEmpty()
                while(not itemsToSend.empty()):
                    result = next(gen)
                    print(result)

        def stop(self):
            if (self.hub_connection):
                self.hub_connection.stop()

        def shutdown(self):
            if (self.hub_connection):
                self.hub_connection.stop()

    iobtHub = SimpleClientHubConnector(iobtBaseURL)

    class TXSender:
        port: str
        tx: str

        def __init__(self, port: str, tx: str) -> None:
            self.port = port
            self.tx = tx

        def send(self):
            print(F"TXSender Sending::: {self.tx}")
            # new messages will restart this port, you must wait until is closes
            # so you better queue the messages and feed them out when you are ready
            open_port = serial.Serial(port, baudrate=57600)
            with ReaderThread(open_port, LoraTransmit) as protocol:
                protocol.tx(self.tx)

            print(F"TXSender Done:::::: {self.tx}")

    # https://pythonhosted.org/pyserial/pyserial_api.html#serial.threaded.ReaderThread
    # https://www.crowdsupply.com/ronoth/lostik

    class LoraReceive(LineReader):

        def connection_made(self, transport):
            print("-------------------------------")
            print("LoraReceive connection made")
            self.transport = transport
            self.send_cmd('sys get ver')
            self.send_cmd('mac pause')
            self.send_cmd('radio set pwr 10')
            self.send_cmd('radio rx 0')
            self.send_cmd("sys set pindig GPIO10 0")

        def turn_on_blue_light(self):
            # print("'''''''''''''''''''''''''''''''''")
            self.send_cmd("sys set pindig GPIO10 1")  # turn on blue

        def turn_off_blue_light(self):
            self.send_cmd("sys set pindig GPIO10 0")  # turn off blue

        def handle_line(self, data):
            if data == "ok" or data == 'busy':
                return
            if data == "radio_err":
                self.send_cmd('radio rx 0')
                return
            if 'RN2903' in data or '4294967245' in data:
                print(F'skipping line because data = {data}')
                return

            print(F'LoraReceive: handling line {data}')
            #self.send_cmd("sys set pindig GPIO10 1", delay=0)

            # Get Hex Data
            #print('getting message data with split " ", 1 [1]')
            message = data.split("  ", 1)[1]
            #print("Hex : %s" % message)

            # Convert to UTF-8
            message_txt = bytes.fromhex(message).decode('utf-8').strip()
            iobtHub.RX(message_txt)
            self.send_cmd('radio rx 0')

        def connection_lost(self, exc):
            if exc:
                print(exc)
            print("LoraReceive port closed")
            print("-------------------------------")

        def send_cmd(self, cmd, delay=.05):
            self.transport.write(('%s\r\n' % cmd).encode('UTF-8'))
            time.sleep(delay)

    class LoraTransmit(LineReader):

        def connection_made(self, transport):
            print("-------------------------------")
            print("LoraTransmit connection made")
            self.transport = transport
            self.send_cmd("sys set pindig GPIO11 0")
            self.send_cmd('sys get ver')
            self.send_cmd('radio get mod')
            self.send_cmd('radio get freq')
            self.send_cmd('radio get sf')
            self.send_cmd('mac pause')
            self.send_cmd('radio set pwr 10')
            self.send_cmd("sys set pindig GPIO11 0")

        def handle_line(self, data):
            # if data == "ok":
            #     return
            print("LoraTransmit handle_line: %s" % data)

        def connection_lost(self, exc):
            if exc:
                print(exc)
            print("LoraTransmit port closed")
            print("-------------------------------")

        def tx(self, message):
            print("Enter tx..............................")
            self.send_cmd("sys set pindig GPIO11 1")
            # print(F"MSG={message}")
            message = message.encode('utf-8').hex()
            print(F"MSG={message}")
            # print(bytes.fromhex(message).decode('utf-8'))

            txmsg = 'radio tx %s' % (message)
            self.send_cmd(txmsg)
            # print("SENT")
            # time.sleep(.3)
            self.send_cmd("sys set pindig GPIO11 0")
            print("Exit  tx..............................")

        def send_cmd(self, cmd, delay=.05):
            # print("SEND: %s" % cmd)
            self.write_line(cmd)
            time.sleep(delay)

    print("Connecting to ", iobtBaseURL)

    return iobtHub


def main():

    hub = LoraTXRX("7020_server", "COM9", "http://localhost:7020")

    hub.start()

    hub.radio_loop_RX()


if __name__ == '__main__':
    main()

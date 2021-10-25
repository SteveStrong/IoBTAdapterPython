import logging
import json
import sys
from typing import Any
import time
import queue


import serial
from serial.threaded import LineReader, ReaderThread

#  https://pypi.org/project/signalrcore/
from signalrcore.hub_connection_builder import HubConnectionBuilder
from signalrcore.protocol.messagepack_protocol import MessagePackHubProtocol




def LoraTXRX(port, iobtBaseURL:str):

    logger = logging.getLogger('LoraTransmit')
    logger.setLevel(logging.DEBUG)  # set logger level
    consoleHandler = logging.StreamHandler(sys.stdout)
    logger.addHandler(consoleHandler)


# https://www.crowdsupply.com/ronoth/lostik

    class LoraTransmit(LineReader):

        def connection_made(self, transport):
            print("-------------------------------")
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

        def handle_line(self, data):
            # if data == "ok":
            #     return
            print("LoraTransmit handle_line: %s" % data)

        def connection_lost(self, exc):
            if exc:
                print(exc)
            print("port closed")
            print("-------------------------------")

        def tx(self, message):
            print("Enter tx..............................")
            self.send_cmd("sys set pindig GPIO11 1")
            #print(F"MSG={message}")
            message = message.encode('utf-8').hex()
            print(F"MSG={message}")
            #print(bytes.fromhex(message).decode('utf-8'))

            txmsg = 'radio tx %s' % (message)
            self.send_cmd(txmsg)
            #print("SENT")
            #time.sleep(.3)
            self.send_cmd("sys set pindig GPIO11 0")
            print("Exit  tx..............................")

        def send_cmd(self, cmd, delay=.01):
            # print("SEND: %s" % cmd)
            self.write_line(cmd)
            time.sleep(delay)

    itemsToSend = queue.Queue()

    def sendQueuedItems():
        items_sent = 0;
        yield F"items sent => {items_sent}";
        while True:
            if (not itemsToSend.empty()):
                item = itemsToSend.get()
                yield "Ready => " + item.tx;
                item.send()
                yield "Sent=> " + item.tx;
                time.sleep(2)
                items_sent += 1
                yield F"items sent => {items_sent}";


    class TXSender:
        port:str
        tx:str

        def  __init__(self, port:str, tx:str) -> None:
            self.port = port
            self.tx = tx;


        def send(self):
            print(F"TXSender Sending::: {self.tx}")
            # new messages will restart this port, you must wait until is closes
            #so you better queue the messages and feed them out when you are ready
            open_port = serial.Serial(port, baudrate=57600)
            with ReaderThread(open_port, LoraTransmit) as protocol:
                protocol.tx(self.tx)
            
            print(F"TXSender Done:::::: {self.tx}")


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

                self.hub_connection.on_open(lambda: print("connection opened and handshake received "))
                self.hub_connection.on_close(lambda: print("connection closed"))

        def start(self):
            try:
                self.hub_connection.start()
                time.sleep(1)
                self.hub_connection.on("Pong", self.receive_pong)
                self.hub_connection.on("Share", self.receive_json)
                self.hub_connection.on("TX", self.receive_TX)

            except:
                print(f"client hub connector exception")
                raise

        def receive_pong(self, pong):
            print("")
            print(f"pong={pong}")

        def receive_json(self, data):
            print("Share: receive_json....")
            # parsed = json.loads(data)
            #print(json.dumps(data[0], indent=3, sort_keys=True))
            # print(f"receive_json={data[0]}")
            pass

        def receive_TX(self, data):
            print("TX: receive_TX....")
            print(json.dumps(data, indent=3, sort_keys=True))

            # new messages will restart this port, you must wait until is closes
            #so you better queue the messages and feed them out when you are ready
            try:
                item = TXSender(port,data[0])
                itemsToSend.put(item)
                print(F"item pushed ${item.tx}")
            except:
                print(f"receive_TX exception")



        def stop(self):
            if (self.hub_connection):
                self.hub_connection.stop()

        def shutdown(self):
            if (self.hub_connection):
                self.hub_connection.stop()


    iobtHub = SimpleClientHubConnector(iobtBaseURL)
    iobtHub.start()

    return sendQueuedItems()
         


def main():

    # seed random number generator

    #iobtBaseURL = "http://centralmodel"
    #iobtBaseURL = "https://iobtweb.azurewebsites.net"
    iobtBaseURL = "http://localhost:7010"

    gen = LoraTXRX("COM8", iobtBaseURL)


    while(True):
        result = next(gen)
        print(result)


if __name__ == '__main__':
    main()

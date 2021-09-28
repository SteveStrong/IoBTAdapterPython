import logging
import sys
from typing import Any
import time

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

def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1

def LoraTXRX(tx_rx_port, baud_rate, iobtBaseURL):

    logger = logging.getLogger('LoraTxRx')
    logger.setLevel(logging.DEBUG)  # set logger level
    consoleHandler = logging.StreamHandler(sys.stdout)
    logger.addHandler(consoleHandler)


    class SimpleClientHubConnector:
        ser: serial.Serial = None
        squireURL: str
        hub_connection: Any = None

        count = 0;
        buffer:str = "";
        listening = True

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

                self.hub_connection.on_open(lambda: print("connection opened signalr is ready"))
                self.hub_connection.on_close(lambda: print("signalr connection closed"))

        def start(self):
            try:
                self.hub_connection.start()
                time.sleep(0.2)
                self.hub_connection.on("Pong", self.receive_pong)
                self.hub_connection.on("ActionStatus", self.receive_status)
                self.hub_connection.on("Share", self.share_json)
                self.hub_connection.on("TX", self.receive_TX)

                self.listening = True
                print(f"event listeners connected")

            except:
                print(f"client hub connector exception")
                raise

        def run(self):
            rx = self.listenSerial();
            while True:
                next(rx)
                if ( self.listening == False):
                    tx = self.sendSerial();
                    next(tx)


        def receive_pong(self, pong):
            print("")
            print(f"pong={pong}")

        def receive_status(self, data):
            print("")
            print(f"data={data[0]}")

        def share_json(self, data):
            print("")
            print(f"share={data[0]}")

        def ping(self, msg: str):
            try:
                #logger.debug(f"Send Ping msg={msg}")
                self.hub_connection.send('Ping', [msg])
            except:
                print(f"Error ${sys.exc_info()[0]}")
                return []

        def RX(self, rx: str):
            try:
                logger.debug(f"Send RX={rx}")
                self.hub_connection.send('RX', [rx])
            except:
                print(f"Error ${sys.exc_info()[0]}")
                return []


        def receive_TX(self, data):
            self.buffer = data[0]
            print("")
            print(f"tx={self.buffer}")
            self.listening = False


        def sendSerial(self):
            try:
                if ( self.ser is not None):
                    self.ser.close()
                
                self.ser = serial.Serial(tx_rx_port, baudrate=baud_rate)
                with ReaderThread(self.ser, LoraTransmit) as protocol:
                    protocol.turn_on_red_light();
                    print(F"Start Transmit on {tx_rx_port}")
                    protocol.tx(self.buffer)
                    yield self.count
                    self.count += 1
                    self.buffer = ""
                    self.listening = False
                    protocol.turn_off_red_light();

                self.ser.close()
                self.ser = None
                print(F"Stop Transmit on {tx_rx_port}")

            except:
                print(f"Error in receive_TX: ${sys.exc_info()[0]}")
           
        def listenSerial(self):
            if ( self.ser is not None):
                self.ser.close()

            self.ser = serial.Serial(tx_rx_port, baudrate=baud_rate)
            with ReaderThread(self.ser, LoraReceive) as protocol:
                protocol.turn_on_blue_light()
                print(F"Start Receive on {tx_rx_port}")
                while(self.listening):
                    yield self.count
                    self.count += 1
        
                protocol.turn_off_blur_light()
            self.ser.close()
            self.ser = None
            print(F"Stop Receive on {tx_rx_port}")

        def stop(self):
            if (self.hub_connection):
                self.hub_connection.stop()

        def shutdown(self):
            if (self.hub_connection):
                self.hub_connection.stop()


    iobtHub = SimpleClientHubConnector(iobtBaseURL)

    #https://pythonhosted.org/pyserial/pyserial_api.html#serial.threaded.ReaderThread
    # https://www.crowdsupply.com/ronoth/lostik

    class LoraTransmit(LineReader):

        def connection_made(self, transport):
            print("LoraTransmit connection made  Turn on RED Light")
            self.transport = transport

            self.send_cmd('sys get ver')
            self.send_cmd('radio get mod')
            self.send_cmd('radio get freq')
            self.send_cmd('radio get sf')
            self.send_cmd('mac pause')
            self.send_cmd('radio set pwr 10')

        def handle_line(self, data):
            if data == "ok":
                return
            print("LoraTransmit RECV: %s" % data)

        def connection_lost(self, exc):
            if exc:
                print(exc)
            print("LoraTransmit port closed")

        def turn_on_red_light(self):
            print("................................")
            self.send_cmd("sys set pindig GPIO11 1") #turn on red

        def turn_off_red_light(self):
            self.send_cmd("sys set pindig GPIO11 0") #turn off red

        def tx(self, message):
            print(F"MSG={message}")
            data = message.encode('utf-8').hex()
            print(F"MSG={data}")
            #print(bytes.fromhex(data).decode('utf-8'))

            txmsg = 'radio tx %s' % (data)
            self.send_cmd(txmsg)


        def send_cmd(self, cmd, delay=.01):
            # print("SEND: %s" % cmd)
            self.write_line(cmd)
            time.sleep(delay)


    class LoraReceive(LineReader):

        def connection_made(self, transport):
            self.transport = transport
            print("LoraReceive  connection made Turn on blue light we are listening")
            self.send_cmd("sys set pindig GPIO10 1")  #turn on blue
            self.send_cmd('sys get ver')
            self.send_cmd('mac pause')
            self.send_cmd('radio set pwr 10')
            self.send_cmd('radio rx 0')

        def turn_on_blue_light(self):
            print("'''''''''''''''''''''''''''''''''")
            self.send_cmd("sys set pindig GPIO10 1") #turn on blue

        def turn_off_blue_light(self):
            self.send_cmd("sys set pindig GPIO10 0") #turn off blue

        def handle_line(self, data):
            print('LoraReceive handling line {0}'.format(data))
            if data == "ok" or data == 'busy':
                return
            if data == "radio_err":
                self.send_cmd('radio rx 0')
                return
            if 'RN2903' in data or '4294967245' in data:
                print('skipping line because data = {0}'.format(data))
                return

            # Get Hex Data
            message = data.split("  ", 1)[1]
            #print("Hex : %s" % message)

            # Convert to UTF-8
            message_txt = bytes.fromhex(message).decode('utf-8').strip()
            #print("Txt : %s" % message_txt)

            #push data into the squire
            iobtHub.RX(message_txt)

            self.send_cmd('radio rx 0')

        def connection_lost(self, exc):
            if exc:
                print(exc)
            print("LoraReceive closing port ")

        def send_cmd(self, cmd, delay=.01):
            self.transport.write(('%s\r\n' % cmd).encode('UTF-8'))
            time.sleep(delay)

    
    print("Connecting to ", iobtBaseURL)



    return iobtHub;



def main():

    #hub = LoraTXRX("COM4", 57600, "http://localhost:6010")
    hub = LoraTXRX("COM4", 57600, "http://localhost:5000")

    def onstart():
        time.sleep(.5)
        print("hub is started...")

    hub.start()
    hub.ping("Lora radio is listening")
    hub.run()


if __name__ == '__main__':
    main()

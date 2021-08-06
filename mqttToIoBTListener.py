from wrappers.MQTTWrapper import MQTTtoIoBTWrapper
from iobtServerRealtime import ClientHubConnector
import sys
import signal

mqttBroker = "demo.iobtlab.com"
username = "techworks"
password = "t3chw0rks"

iobtBaseURL = "https://iobtweb.azurewebsites.net"

def signal_handler(sig, frame):
    sys.exit(0)   

if __name__ == '__main__':
    iobtHub = ClientHubConnector(iobtBaseURL)

    mqttHub = MQTTtoIoBTWrapper(mqttBroker, 1883)
    mqttHub.iobt_hub = iobtHub

    mqttHub.start()

    mqttHub.do_loop()

    signal.pause()
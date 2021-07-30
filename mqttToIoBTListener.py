from iobt.MQTTWrapper import MQTTWrapper
from iobt.iobtServerRealtime import ClientHubConnector

mqttBroker = " demo.iobtlab.com"
username = "techworks"
password = "t3chw0rks"

iobtBaseURL = "https://iobtweb.azurewebsites.net"

if __name__ == '__main__':
    iobtHub = ClientHubConnector(iobtBaseURL)

    mqttHub = MQTTWrapper(mqttBroker, "1883")
    mqttHub.iobt_hub = iobtHub

    mqttHub.start()

    mqttHub.do_loop()

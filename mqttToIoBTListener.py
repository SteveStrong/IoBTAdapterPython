from .wrappers.MQTTWrapper import MQTTtoIoBTWrapper
from .iobtServerRealtime import ClientHubConnector

mqttBroker = "demo.iobtlab.com"
username = "techworks"
password = "t3chw0rks"

iobtBaseURL = "https://iobtweb.azurewebsites.net"


def main():
    iobtHub = ClientHubConnector(iobtBaseURL)

    mqttHub = MQTTtoIoBTWrapper(mqttBroker, 1883)
    mqttHub.iobt_hub = iobtHub

    mqttHub.start()

    mqttHub.do_loop()

    # cross-platform way to pause python execution.  signal is not available in windows
    input("Press the <Enter> key or <ctrl-C> to continue...")


# if __name__ == '__main__':
main()

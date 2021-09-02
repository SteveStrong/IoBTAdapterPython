import sys
import signal
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

    json = {
        
    }

    mqttHub.start()

    mqttHub.do_loop()

    def end_of_processing(signal_number, stack_frame):
        print(f"Exiting")
        mqttHub.client.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT, end_of_processing)
    # cross-platform way to pause python execution.  signal is not available in windows
    input("\nPress the <Enter> key or <ctrl-C> to continue...\n\n")


# if __name__ == '__main__':
main()

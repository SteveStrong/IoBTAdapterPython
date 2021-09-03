import sys
import time
import signal
from .wrappers.MQTTIoBTWrapper import MQTTtoIoBTWrapper
from .iobtServerRealtime import IoBTClientHubConnector


mqttBroker = "mqttbrokerapi"
# mqttBroker = "demo.iobtlab.com"
# username = "techworks"
# password = "t3chw0rks"

# iobtBaseURL = "https://iobtweb.azurewebsites.net"
iobtBaseURL = "http://centralmodelapi"


def main():
    iobtHub = IoBTClientHubConnector(iobtBaseURL)

    mqttHub = MQTTtoIoBTWrapper(mqttBroker, 1883)
    mqttHub.iobt_hub = iobtHub

    mqttHub.start()

    mqttHub.do_loop()

    def end_of_processing(signal_number, stack_frame):
        print(f"Exiting")
        mqttHub.client.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT, end_of_processing)
    # cross-platform way to pause python execution.  signal is not available in windows
    while True:
        # TODO: is there a better way to constantly listen?
        time.sleep(0.1)


# if __name__ == '__main__':
main()

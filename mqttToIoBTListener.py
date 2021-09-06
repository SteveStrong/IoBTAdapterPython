import sys
import time
import signal
from .wrappers.MQTTWrapper import MQTTtoIoBTWrapper
from .iobtServerRealtime import ClientHubConnector


mqttBroker = "mqttbroker"
iobtBaseURL = "http://centralmodel"


def main():
    iobtHub = ClientHubConnector(iobtBaseURL)
    iobtHub.start()

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

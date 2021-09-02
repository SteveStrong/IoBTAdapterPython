import sys
import time
import signal
from .wrappers.MQTTWrapper import MQTTtoIoBTWrapper
from .iobtServerRealtime import IoBTClientHubConnector
from .iobtServerRest import IobtServerRest

mqttBroker = "demo.iobtlab.com"
username = "techworks"
password = "t3chw0rks"

# iobtBaseURL = "https://iobtweb.azurewebsites.net"
# iobtBaseURL = "http://localhost:8000"
# iobtBaseURL = "http://0.0.0.0:8000"
# iobtBaseURL = "http://127.0.0.1:8080"
iobtBaseURL = "http://iobtserver"


def main():
    print(f"Start of main")
    iobtHub = IoBTClientHubConnector(iobtBaseURL)
    iobtHub.start()
    print(f"Started iobtHub")

    iobtRest = IobtServerRest(iobtBaseURL)
    print(f"Started iobtRest")
    iobtRest.ping()

    def end_of_processing(signal_number, stack_frame):
        print(f"Exiting")
        sys.exit(0)

    signal.signal(signal.SIGINT, end_of_processing)

    while True:
        # TODO: is there a better way to constantly listen?
        time.sleep(0.1)


# if __name__ == '__main__':
main()

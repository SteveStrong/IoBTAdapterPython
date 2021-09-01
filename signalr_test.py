import sys
import time
import signal
import logging
from .wrappers.MQTTWrapper import MQTTtoIoBTWrapper
from .iobtServerRealtime import ClientHubConnector
from .iobtServerRest import IobtServerRest

logger = logging.getLogger('signalr_test')
logger.setLevel(logging.DEBUG)  # set logger level
consoleHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(consoleHandler)

# iobtBaseURL = "https://iobtweb.azurewebsites.net"
iobtBaseURL = "http://centralmodelapi"


def main():
    logger.debug(f"Start of main")
    # print(f"Start of main")
    iobtHub = ClientHubConnector(iobtBaseURL)
    iobtHub.start()
    print(f"Started iobtHub")

    iobtRest = IobtServerRest(iobtBaseURL)
    logger.debug(f"Started iobtRest")
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

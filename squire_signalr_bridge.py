import sys
import time
import signal
import logging

# import turfpy
# from turfpy.measurement import destination
# from geojson import Point, Feature


from .iobtServerSync import IoBTServerHubConnector

logger = logging.getLogger('squire_signalr_bridge')
logger.setLevel(logging.DEBUG)  # set logger level

consoleHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(consoleHandler)

#  https://github.com/omanges/turfpy
#  https://pypi.org/project/turfpy/
#  https://github.com/omanges/turfpy/blob/master/measurements.md

iobtBaseURL = "http://centralmodel"
iobtBaseURL1 = "https://iobtsquire1.azurewebsites.net"
iobtBaseURL2 = "https://iobtweb.azurewebsites.net"

iobtBaseURL1 = "http://localhost:5000"

class ServerHubHooks():

    def on_ping(self, payload):
        logger.debug(f"on_ping={payload}")
        print(f"on_ping={payload}")

    def on_position(self, payload):
        logger.debug(f"on_position={payload}")
        print(f"on_position={payload}")

    def on_send(self, payload):
        logger.debug(f"on_send={payload}")
        print(f"on_send={payload}")

    def on_monitor(self, payload):
        logger.debug(f"on_monitor={payload}")
        print(f"on_monitor={payload}")

def main():

    iobtHub1 = IoBTServerHubConnector(iobtBaseURL1)
    #iobtHub2 = IoBTServerHubConnector(iobtBaseURL1)

    hooks =  ServerHubHooks()
    iobtHub1.start(hooks)
    #iobtHub2.start( ServerHubHooks())
        
    def end_of_processing(signal_number, stack_frame):
        print(f"Exiting")
        iobtHub1.stop()
        #iobtHub2.stop()
        sys.exit(0)

    while(True):
        print('.')
        time.sleep(1)
        signal.signal(signal.SIGINT, end_of_processing)
        # cross-platform way to pause python execution.  signal is not available in windows
        input("\nPress the <Enter> key or <ctrl-C> to continue...\n\n")





# if __name__ == '__main__':
main()

from models.udto_message import UDTO_Position
import time
import sys
import signal

import turfpy
from turfpy.measurement import destination
from geojson import Point, Feature


from iobtServerRealtime import IoBTClientHubConnector


#  https://github.com/omanges/turfpy
#  https://pypi.org/project/turfpy/
#  https://github.com/omanges/turfpy/blob/master/measurements.md

iobtBaseURL = "http://centralmodelapi"
iobtBaseURL = "https://iobtweb.azurewebsites.net"

def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1

def circle_sequence():
    origin = Feature(geometry=Point([-75.343, 39.984]))
    distance = .5
    bearing = 10
    options = {'units': 'km'}
    while True:
        result = destination(origin,distance,bearing,options)
        coord = result.geometry.coordinates
        yield coord
        origin = Feature(geometry=Point(coord))


def main():
    iobtHub = IoBTClientHubConnector(iobtBaseURL)

    iobtHub.start()

    iobtHub.ping("Simulation starting")

    gen = circle_sequence()
    while(True):
        result = next(gen)
        payload = {
            'panId': 'Steve',
            'lat': result[1],
            'lng': result[0],
            'alt': 0,
        }

        pos = UDTO_Position(payload)
        iobtHub.position(pos)
        print(payload)
        time.sleep(1) # Sleep for 1 seconds



    def end_of_processing(signal_number, stack_frame):
        print(f"Exiting")
        # iobtHub.client.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT, end_of_processing)
    # cross-platform way to pause python execution.  signal is not available in windows
    input("\nPress the <Enter> key or <ctrl-C> to continue...\n\n")


if __name__ == '__main__':
    main()

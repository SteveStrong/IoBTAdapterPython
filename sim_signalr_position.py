from models.udto_message import UDTO_Position
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

def main():
    iobtHub = IoBTClientHubConnector(iobtBaseURL)


    origin = Feature(geometry=Point([-75.343, 39.984]))
    distance = 50
    bearing = 90
    options = {'units': 'km'}
    result = destination(origin,distance,bearing,options)
    coord = result.geometry.coordinates

    payload = {
        'panId': 'Steve',
        'lat': coord[1],
        'lng': coord[0],
        'alt': 0,
    }

    pos = UDTO_Position(payload)

    print(pos)

    iobtHub.start()

    iobtHub.ping("Simulation starting")

    iobtHub.position(pos)



    def end_of_processing(signal_number, stack_frame):
        print(f"Exiting")
        # iobtHub.client.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT, end_of_processing)
    # cross-platform way to pause python execution.  signal is not available in windows
    input("\nPress the <Enter> key or <ctrl-C> to continue...\n\n")


if __name__ == '__main__':
    main()

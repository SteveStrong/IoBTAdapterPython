from .models.udto_message import UDTO_Position
import time
import sys
import signal

import turfpy
from turfpy.measurement import destination
from geojson import Point, Feature


from .iobtServerRealtime import IoBTClientHubConnector


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


def circle_sequence(dist):
    origin = Feature(geometry=Point([-75.343, 39.984]))
    distance = dist
    bearing = 80
    options = {'units': 'km'}
    while True:
        result = destination(origin, distance, bearing, options)
        coord = result.geometry.coordinates
        yield coord
        origin = Feature(geometry=Point(coord))
        bearing += 10


def main():
    iobtHub = IoBTClientHubConnector(iobtBaseURL)

    iobtHub.start()

    iobtHub.ping("Simulation starting")

    gen1 = circle_sequence(0.05)
    gen2 = circle_sequence(0.15)
    while(True):
        result = next(gen2)
        payload = {
            'panId': 'Steve',
            'lat': result[1],
            'lng': result[0],
            'alt': 0,
        }

        pos = UDTO_Position(payload)
        iobtHub.position(pos)

        result = next(gen1)
        payload = {
            'panId': 'Greg',
            'lat': result[1],
            'lng': result[0],
            'alt': 0,
        }

        pos = UDTO_Position(payload)
        iobtHub.position(pos)
        print(payload)
        time.sleep(1)  # Sleep for 1 seconds


# if __name__ == '__main__':
main()

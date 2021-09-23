from .models.udto_message import UDTO_Position
import time
import uuid
from random import seed
from random import randint

import turfpy
from turfpy.measurement import destination
from geojson import Point, Feature


from .iobtServerRealtime import IoBTClientHubConnector


#  https://github.com/omanges/turfpy
#  https://pypi.org/project/turfpy/
#  https://github.com/omanges/turfpy/blob/master/measurements.md

iobtBaseURL = "http://centralmodel"
# iobtBaseURL = "https://iobtsquire1.azurewebsites.net"


def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1


def circle_sequence(dist, bear, bear_delta):
    origin = Feature(geometry=Point([-75.343, 39.984]))
    distance = dist
    bearing = bear
    options = {'units': 'km'}
    while True:
        result = destination(origin, distance, bearing, options)
        coord = result.geometry.coordinates
        yield coord
        origin = Feature(geometry=Point(coord))
        bearing += bear_delta


def main():

    # seed random number generator
    seed(1)

    iobtHub = IoBTClientHubConnector(iobtBaseURL)

    iobtHub.start()

    iobtHub.ping("Simulation starting")

    gen1 = circle_sequence(0.05, randint(10, 80), randint(1, 10))
    uuid1 = f"{uuid.uuid4()}"
    gen2 = circle_sequence(0.10, randint(80, 130), randint(1, 10))
    uuid2 = f"{uuid.uuid4()}"
    time.sleep(randint(10, 60))
    while(True):
        result = next(gen1)
        payload = {
            'sourceGuid': uuid1,
            'panId': 'Steve',
            'lat': result[1],
            'lng': result[0],
            'alt': 0,
        }

        pos = UDTO_Position(payload)
        iobtHub.position(pos)
        print(payload)

        result = next(gen2)
        payload = {
            'sourceGuid': uuid2,
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

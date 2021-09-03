import sys
import signal
import turfpy

from turfpy.measurement import destination
from geojson import Point, Feature


from .wrappers.MQTTPublisherWrapper import MQTTPublisherWrapper

#  https://github.com/omanges/turfpy
#  https://pypi.org/project/turfpy/
#  https://github.com/omanges/turfpy/blob/master/measurements.md

mqttBroker = "demo.iobtlab.com"


def main():
    mqttHub = MQTTPublisherWrapper(mqttBroker, 1883)


    origin = Feature(geometry=Point([-75.343, 39.984]))
    distance = 50
    bearing = 90
    options = {'units': 'mi'}
    result = destination(origin,distance,bearing,options)

    payload = {

    }

    mqttHub.start()

    ##mqttHub.do_loop()

    mqttHub.publish("iobt/udto/Position",payload)


    def end_of_processing(signal_number, stack_frame):
        print(f"Exiting")
        mqttHub.client.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT, end_of_processing)
    # cross-platform way to pause python execution.  signal is not available in windows
    input("\nPress the <Enter> key or <ctrl-C> to continue...\n\n")


if __name__ == '__main__':
    main()

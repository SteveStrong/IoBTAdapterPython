import sys
import signal

from .wrappers.MQTTPublisherWrapper import MQTTPublisherWrapper



mqttBroker = "demo.iobtlab.com"


def main():
    mqttHub = MQTTPublisherWrapper(mqttBroker, 1883)


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

from typing import Any
import time
import serial


def main():

    data = "Hello, World"
    while(True):
        serialstream = serial.Serial('COM8', 115200)
        serialstream.write(bytes(data.encode('UTF-8')))
        time.sleep(3)
        serialstream.close()
        time.sleep(3)


if __name__ == '__main__':
    main()

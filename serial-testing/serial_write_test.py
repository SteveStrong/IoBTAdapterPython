import serial
import time

serialstream = serial.Serial('/dev/tty.usbmodem11301',115200)

#serialstream.write(bytes(data.encode('UTF-8')))


serialstream.write(bytes("".encode('UTF-8')))

time.sleep(0.05)

data = serialstream.readline()

print(data)

serialstream.close()
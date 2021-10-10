import serial
import time
arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.read()
    return data


while True:
    num = input("Enter a number: ")  # Taking input from user
    value = write_read(num)
    print(value)  # printing the value

# import serial
# import time


# def main():
#     message = "Position,4debd695-0fa5-421f-ab7d-49131ff744eb,2021-10-08T21:02:22.180Z,Squire_TestSquire1,38.78264,-77.01506000000002,0.001"
#     arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)
#     i = 0

#     def write_read(x):
#         payload = bytes(x, 'utf-8')
#         arduino.write(payload)
#         time.sleep(0.05)
#         data = arduino.readline()
#         test_str = bytes.decode(data, 'utf-8')
#         return test_str
#     while True:
#         # while i < 3:
#         # num = input("Enter a number: ")  # Taking input from user
#         value = write_read(message)
#         print(value)  # printing the value


# if __name__ == '__main__':
#     main()

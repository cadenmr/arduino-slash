import serial
import time

arduino = serial.Serial("/dev/rfcomm0", baudrate=115200)

while True:
    arduino.write('+0000,+0000'.encode())
    time.sleep(0.1)
    arduino.write('-1000,+0000'.encode())
    time.sleep(0.1)
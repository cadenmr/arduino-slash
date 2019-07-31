import serial
import time
import controller
import signal

# Update & poll rate
timing = 0.01
run = True


def sigint_handler(*_):
    global run

    print(" pressed, quitting...")
    run = False
    controller.disconnect()

# Try connection to wired and wireless serial ports
try:
    slash = serial.Serial('/dev/rfcomm0', baudrate=115200)  # First, try wireless
    print('Connected to Arduino via Bluetooth')
except serial.serialutil.SerialException:
    try:
        slash = serial.Serial('/dev/ttyACM0', baudrate=115200)  # If wireless is unavaliable, try wired
        print('Connected to Arduino via wire')
    except serial.serialutil.SerialException: # If neither is found, print error and quit
        print("Arduino not found. Please check connection. (Did you rfcomm bind first?)")
        print("Tried: /dev/rfcomm0, /dev/ttyACM0")
        quit()

controller = controller.Controller(10000)  # Xbox 360 Controller using the controller class
signal.signal(signal.SIGINT, sigint_handler)

print('Ready')

while run:
    controller.read_controller()  # Read data from controller
    slash.write(controller.get_parsed_string().encode())  # Get controller's last read data, encode it, send it

    time.sleep(timing)  # Prevent constant polling and 100% CPU usage

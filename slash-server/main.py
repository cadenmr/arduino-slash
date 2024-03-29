import serial
from time import sleep
import controller
import signal

configfile = open('server.conf', 't+r')  # Open configfile for text reading
config_list = [ d.replace('\n', '') for d in configfile ]  # Parse the file
timing, baudrate, *_ = config_list  # Unpack the parsed list
timing = float(timing.split()[2])  # Grab the value
baudrate = float(baudrate.split()[2])
configfile.close()  # Close the config file

def sigint_handler(*_):  # SIGINT handler function
    print(" pressed, quitting...")
    controller.disconnect()  # Disconnect the controller
    quit()  # Quit

# Try connection to wired and wireless serial ports
try:
    slash = serial.Serial('/dev/rfcomm0', baudrate=baudrate)  # First, try wireless
    print('Connected to Arduino via Bluetooth')
except serial.serialutil.SerialException:
    try:
        slash = serial.Serial('/dev/ttyACM0', baudrate=baudrate)  # If wireless is unavaliable, try wired
        print('Connected to Arduino via wire')
    except serial.serialutil.SerialException: # If neither is found, print error and quit
        print("Arduino not found. Please check connection. (Did you rfcomm bind first?)")
        print("Tried: /dev/rfcomm0, /dev/ttyACM0")
        quit()

controller = controller.Controller(10000)  # Xbox 360 Controller using the controller class
signal.signal(signal.SIGINT, sigint_handler)  # SIGINT handler setup

sleep(2)

slash.write('+1000,+0000'.encode())
sleep(0.3)
slash.write('-1000,+0000'.encode())
sleep(0.3)
slash.write('+1000,+0000'.encode())
sleep(0.3)
slash.write('-1000,+0000'.encode())
sleep(0.3)
slash.write('+0000,+0000'.encode())
sleep(0.5)
slash.write('+0000,+0047'.encode()) # Arm the ESC
sleep(0.5)

print('Ready')

while True:
    controller.read_controller()  # Read data from controller
    slash.write(controller.get_parsed_string().encode())  # Get controller's last read data, encode it, send it

    sleep(timing)  # Prevent constant polling and 100% CPU usage

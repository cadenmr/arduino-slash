import serial
import time
import controller

# Amount of time to wait to keep bluetooth managable
timing = 0.05

# Define objects
slash = serial.Serial('/dev/ttyACM0', baudrate=115200) # initialize serial
controller = controller.Controller(10000)

while True:
    controller.read_controller()
    slash.write(controller.get_parsed_string().encode())
    slash.flush()

    print(controller.get_parsed_string())

    time.sleep(timing)
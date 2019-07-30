# Simple Xbox 360 controller unit test

import controller
import time

controller = controller.Controller(10000)

while True:
    controller.read_controller()
    print(controller.get_parsed_string())
    time.sleep(0.05)
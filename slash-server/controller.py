import xbox


class Controller:
    def __init__(self, deadzone=10000):  # Constructor. Takes in a joystick deadzone.
        self.joy = xbox.Joystick()
        self.joyDeadzone = deadzone

    def __get_state(self, num):
        # Returns the state of a float, + or -

        if num < 0:
            return '-'
        else:
            return '+'

    def __get_trigger_state(self):
        # Gets the trigger's state, + for rightTrigger, - for leftTrigger

        if self.leftTrigger > 0:
            return '-'
        else:
            return '+'

    def __get_trigger_position(self):
        # Selects the correct trigger and outputs its value

        if self.leftTrigger > 0:
            return self.leftTrigger
        else:
            return self.rightTrigger

    def __correct_length(self, data):
        # Makes sure the data passed in is always 4 digits long. Converts to str() unconditionally

        if len(str(data)) < 4:
            if len(str(data)) < 3:
                return str(data) + '00'
            else:
                return str(data) + '0'
        else:
            return str(data)

    def __parse_input(self, round_amount):
        # Parses the input and builds a standard-compliant string

        self.leftJoyX = round(self.leftJoyX, round_amount)
        self.leftTrigger = round(self.leftTrigger, round_amount)
        self.rightTrigger = round(self.rightTrigger, round_amount)

        self.leftJoyXState = self.__get_state(self.leftJoyX)
        self.triggerState = self.__get_trigger_state()

        self.final_leftJoyX = str(self.leftJoyX).replace('.', '').replace('-','')
        self.final_trigger  = str(self.__get_trigger_position()).replace('.','').replace('-','')

        self.final_leftJoyX = self.__correct_length(self.final_leftJoyX)
        self.final_trigger = self.__correct_length(self.final_trigger)

        self.final_output = f'{self.leftJoyXState}{self.final_leftJoyX},{self.triggerState}{self.final_trigger}'

    def read_controller(self):
        # Reads the controller's data

        self.leftJoyX = self.joy.leftX(self.joyDeadzone)
        self.leftTrigger = self.joy.leftTrigger()
        self.rightTrigger = self.joy.rightTrigger()

        self.__parse_input(3)

    def get_parsed_string(self):
        # Gets standard-compliant string

        return self.final_output

    def disconnect(self):
        # Disconnect controller

        self.joy.close()

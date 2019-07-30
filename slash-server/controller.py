import xbox


class Controller:
    def __init__(self, deadzone): # Constructor. Take no values.
        self.joy = xbox.Joystick()
        self.joyDeadzone = deadzone

    def __get_state(self, num):
        if num < 0:
            return '-'
        else:
            return '+'

    def __get_trigger_state(self):
        if self.leftTrigger > 0:
            return '-'
        else:
            return '+'

    def __get_trigger_position(self):
        if self.leftTrigger > 0:
            return self.leftTrigger
        else:
            return self.rightTrigger

    # W: This will forcefully convert to str()
    def __correct_length(self, data):
        if len(str(data)) < 4:
            if len(str(data)) < 3:
                return str(data) + '00'
            else:
                return str(data) + '0'
        else:
            return str(data)

    def __parse_input(self, round_amount):
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
        self.leftJoyX = self.joy.leftX(self.joyDeadzone)
        self.leftTrigger = self.joy.leftTrigger()
        self.rightTrigger = self.joy.rightTrigger()

        self.__parse_input(3)

    def get_parsed_string(self):
        return self.final_output

    def disconnect(self):
        self.joy.close()
        return 'Safe to disconnect'

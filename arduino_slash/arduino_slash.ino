// Provides computer control for the 1/16 Slash VXL 4x4 RC car
// Arduino is intended to be placed in between the reciever and the ESC and servo

#include <Servo.h>
#include <SoftwareSerial.h>

#define STEER_INPUT 2
#define THRO_INPUT 3
#define THRO_OUTPUT 4
#define STEER_OUTPUT 5

volatile int pwm_value_1 = 0;
volatile int prev_time_1 = 0;
volatile int pwm_value_2 = 0;
volatile int prev_time_2 = 0;

char steer_state_byte = '+';
char thro_state_byte = '+';

char command_byte_steer_ones = '0';
char command_byte_steer_tens = '0';
char command_byte_steer_hunds = '0';
char command_byte_steer_thous = '0';

char command_byte_thro_ones = '0';
char command_byte_thro_tens = '0';
char command_byte_thro_hunds = '0';
char command_byte_thro_thous = '0';

int steer_command;
int thro_command;

String recieved_data;

Servo STEER_SERVO;
Servo ESC;
SoftwareSerial Bluetooth(10, 9); // RX, TX

void setup() {
  STEER_SERVO.attach(STEER_OUTPUT);
  ESC.attach(THRO_OUTPUT);

  STEER_SERVO.write(90);
  //ESC.write(90);

  Serial.begin(115200);
  Serial.setTimeout(2);
  Bluetooth.begin(115200);
  Bluetooth.setTimeout(1);

  //attachInterrupt(0, rising_1, RISING);
  //attachInterrupt(1, rising_2, RISING);
}

void loop() {
  read_serial_data();
  
  //STEER_SERVO.write(pwm_value_1);
  STEER_SERVO.write(map(steer_command, -2000, 2000, 0, 180));
  ESC.write(map(thro_command, -1000, 1000, 950, 1950));

  //delay(5);
}

// Interrupt functions
void rising_1() {
  attachInterrupt(0, falling_1, FALLING);
  prev_time_1 = micros();
}
 
void falling_1() {
  attachInterrupt(0, rising_1, RISING);
  pwm_value_1 = micros()-prev_time_1;
}

void rising_2() {
  attachInterrupt(1, falling_2, FALLING);
  prev_time_2 = micros();
}
 
void falling_2() {
  attachInterrupt(1, rising_2, RISING);
  pwm_value_2 = micros()-prev_time_2;
}

// Serial data input in accordance to data struct
// +-0000,+-0000
//  steer,throttle
void read_serial_data() {
  if (Serial.available()) {
    recieved_data = Serial.readString();

    thro_state_byte = char(recieved_data[6]);
    steer_state_byte = char(recieved_data[0]);
    
    command_byte_steer_ones = char(recieved_data[1]);
    command_byte_steer_tens = char(recieved_data[2]);
    command_byte_steer_hunds = char(recieved_data[3]);
    command_byte_steer_thous = char(recieved_data[4]);

    steer_command = ((command_byte_steer_ones - '0') * 1000) + ((command_byte_steer_tens - '0') * 100) + ((command_byte_steer_hunds - '0') * 10) + (command_byte_steer_thous - '0');

    if (steer_state_byte == '-') {
      steer_command = steer_command - (steer_command * 2);
    }

    command_byte_thro_ones = char(recieved_data[7]);
    command_byte_thro_tens = char(recieved_data[8]);
    command_byte_thro_hunds = char(recieved_data[9]);
    command_byte_thro_thous = char(recieved_data[10]);

    thro_command = ((command_byte_thro_ones - '0') * 1000) + ((command_byte_thro_tens - '0') * 100) + ((command_byte_thro_hunds - '0') * 10) + (command_byte_thro_thous - '0');

    if (thro_state_byte == '-') {
      thro_command = thro_command - (thro_command * 2);
    }

    //Serial.println(recieved_data);
    
    recieved_data = "";
    //Serial.flush();
  }
}

// esc speed setter shortcut with deadzone
void esc_set_speed(int value) {
  if (value > 1950) {
    ESC.write(2000);
  } else {
    ESC.write(value);
  }
}

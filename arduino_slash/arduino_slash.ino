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

// DEFINE OBJECTS
Servo STEER_SERVO;
Servo ESC;
SoftwareSerial Bluetooth(10, 9);

void setup() {
  //pinMode(THRO_OUTPUT, OUTPUT);
  STEER_SERVO.attach(STEER_OUTPUT);
  ESC.attach(THRO_OUTPUT);

  Serial.begin(9600);
  Bluetooth.begin(9600);

  attachInterrupt(0, rising_1, RISING);
  attachInterrupt(1, rising_2, RISING);
}

void loop() {
  STEER_SERVO.write(pwm_value_1);
  //Serial.println("Steer: " + String(pwm_value_1));

  //Serial.println("Throttle: " + String(pwm_value_2));
  ESC.write(pwm_value_2);
}

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

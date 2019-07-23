// Provides computer control for the 1/16 Slash VXL 4x4 RC car
// Arduino is intended to be placed in between the reciever and the ESC and servo

#include <Servo.h>

// PIN ASSIGNMENTS
int THRO_INPUT = 3;
int STEER_INPUT = 5;
int THRO_OUTPUT = 6;
int STEER_OUTPUT = 9;

// DEFINE VARIABLES
int THRO_POSITION = 0;
int STEER_POSITION = 0;
int SERIAL_DATA;
int SERIAL_CHAR;

// DEFINE OBJECTS
Servo STEER_SERVO;

void setup() {
  pinMode(THRO_INPUT, INPUT);
  pinMode(THRO_OUTPUT, OUTPUT);
  pinMode(STEER_INPUT, INPUT);
  STEER_SERVO.attach(STEER_OUTPUT);

  Serial.begin(9600);
}

void loop() {
  STEER_POSITION = pulseIn(STEER_INPUT, HIGH);
  //Serial.println(map(STEER_POSITION, 970, 1960, 0, 180));
  STEER_SERVO.write(map(STEER_POSITION, 970, 1960, 0, 180));

  THRO_POSITION = pulseIn(THRO_INPUT, HIGH);
  Serial.println(THRO_POSITION);
}

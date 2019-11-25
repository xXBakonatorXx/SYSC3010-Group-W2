#include <AFMotor.h>

AF_Stepper Stepper1(48,2); //48 steps per rev

void setup() {
  // put your setup code here, to run once:
  Stepper1.setSpeed(100); //Set motor1 to 10 rpm
}

void loop() {
  // put your main code here, to run repeatedly:
  Stepper1.step(100, FORWARD, SINGLE); //Takes one step forward using double coil stepping
  delay(100);
}

#include <AFMotor.h>
#include <stdint.h>

#define PIN0 0
#define PIN1 1
#define PIN2 2

// config motors through motor shield
AF_DCMotor motor1(1, MOTOR12_1KHZ);
AF_DCMotor motor2(2, MOTOR12_1KHZ);

uint8_t val0  = 0;
uint8_t val1  = 0;
uint8_t val2  = 0;
uint8_t w_sum = 0;
uint8_t sum   = 0;
uint8_t ref   = 2; // referance for the middle sensor
float   avg   = 0;

void setup() {
  Serial.begin(9600);
  pinMode(PIN0, INPUT);
  pinMode(PIN1, INPUT);
  pinMode(PIN2, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  val0  = (uint8_t)digitalRead(PIN0);
  val1  = (uint8_t)digitalRead(PIN1);
  val2  = (uint8_t)digitalRead(PIN2);

  // calculates position of line under the sensors
  w_sum = (uint8_t)(val0 * 1 + val1 * 2 + val2 * 3);
  sum   = (uint8_t)(val0 + val1 + val2);
  avg   = (float)(w_sum / sum);

  pos   = ref - avg;

  Serial.print(pos);
}

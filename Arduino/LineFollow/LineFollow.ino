#include <control.h>

#include <PID_v1.h>
#include <AFMotor.h>

#define IR_PIN 2
#define N_SENSORS 5
#define SPEED 75
#define FACTOR 10
#define CENTER 3

// ir sensor values
int ir_values[N_SENSORS];

// line position
double w_sum = NULL;
double sum   = NULL;
double avg   = NULL;
double motor_l = NULL;
double motor_r = NULL;

// config motors through motor shield
AF_DCMotor motor1(1, MOTOR12_1KHZ);
AF_DCMotor motor2(2, MOTOR12_1KHZ);

// setup pid controller
/*PID ladPID(&input, &output, &setpoint, Kp, Ki, Kd, DIRECT);*/

void setup() {
  Serial.begin(9600);

  // the value pid adjusts towards
  setpoint = 0;

  for (int pin = IR_PIN; pin < IR_PIN + N_SENSORS; pin++) {
    pinMode(pin, INPUT);
  }
}

void loop() {
  // read ir sensors. 1 while no object, 0 while obeject (1 when line is underneath)
  for (int sensor = 0; sensor < N_SENSORS; sensor++) {
    ir_values[sensor] = (double)digitalRead(sensor + IR_PIN);
  }

  sum = 0;
  w_sum = 0;
  avg = get_position(ir_values, N_SENSORS, &w_sum, &sum);
  
  output = CENTER - avg;
  control(output, FACTOR, SPEED, &motor_l, &motor_r);

  Serial.print(motor_l);
  Serial.println(motor_r);  
}

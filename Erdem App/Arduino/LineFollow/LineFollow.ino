#include <control.h>
#include <AFMotor.h>

// ultrasonic pins
#define ULTRASONIC_TX 8
#define ULTRASONIC_RX 7
#define ULTRASONIC_THRESHOLD 10

// ir pins
#define IR_PIN 2
#define N_IR_SENSORS 5

// line follow constants
#define SPEED 75
#define FACTOR 10
#define CENTER 3

// ir sensor values
int ir_values[N_IR_SENSORS];

// line position
double w_sum = NULL;
double sum   = NULL;
double avg   = NULL;
double motor_l = NULL;
double motor_r = NULL;

// obstacle
double distance = 0;
double obstacle = false;

// config motors through motor shield
AF_DCMotor motor1(1, MOTOR12_1KHZ);
AF_DCMotor motor2(2, MOTOR12_1KHZ);

void read_IR_sensors() {
  // read ir sensors. 1 while no object, 0 while obeject (1 when line is underneath)
  for (int sensor = 0; sensor < N_IR_SENSORS; sensor++) {
    ir_values[sensor] = (double)digitalRead(sensor + IR_PIN);
  }
}

double read_ultrasonic() {
  digitalWrite(ULTRASONIC_TX, LOW);
  delayMicroseconds(2);

  digitalWrite(ULTRASONIC_TX, HIGH);
  delayMicroseconds(10);
  digitalWrite(ULTRASONIC_TX, LOW);

  return pulseIn(ULTRASONIC_RX, HIGH) * 0.034 / 2;
}

void setup() {
  Serial.begin(9600);

  for (int pin = IR_PIN; pin < IR_PIN + N_IR_SENSORS; pin++) {
    pinMode(pin, INPUT);
  }

  pinMode(ULTRASONIC_TX, OUTPUT);
  pinMode(ULTRASONIC_RX, INPUT);
}

void loop() {
  //object avoidance
  distance = read_ultrasonic();
  obstacle = detect_object(ULTRASONIC_THRESHOLD, distance);
  if (obstacle) {
    motor_l = 0;
    motor_r = 0;
    Serial.println("OH shit an obsticle!!!");
  } else {
    
    //Line Follow
    read_IR_sensors();
    avg = get_position(ir_values, N_IR_SENSORS, &w_sum, &sum);
    control_motors(CENTER - avg, FACTOR, SPEED, &motor_l, &motor_r);
    if (isnan(motor_l) || isnan(motor_r)) {
      motor_l = -99;
      motor_r = -99;
      Serial.println("Recalculating...");
    }
    Serial.print(motor_l);
    Serial.print("% ");
    Serial.print(motor_r);
    Serial.println("%");
  }

  delay(500);
}

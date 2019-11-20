#include <control.h>
#include <AFMotor.h>

// ultrasonic pins
/*
 * ULTRASONIC_THRESHOLD is the minimum distance at which 
 * an object can be before it is detected as an obstacle
 */
#define ULTRASONIC_TX 8
#define ULTRASONIC_RX 7
#define ULTRASONIC_THRESHOLD 10

// ir pins
/*
 * Assuming all ir sensors are wired next to one another
 * IR_PIN is the values of the first pin, and N_IR_SENSORS
 * is the number of ir sensors.
 * 
 * Allows for easy changing of the number of sensors.
 */
#define IR_PIN 2
#define N_IR_SENSORS 5

// line follow constants
/*
 * CENTER is the position of the middle of the LAD Unit
 * used for controling motor.
 */
#define MOTOR_SPEED 75
#define STEERING_SENSITIVITY 10
#define CENTER (1 + N_IR_SENSORS) / 2

// ir sensor values
int ir_values[N_IR_SENSORS];

// line position
double w_sum = NULL;
double sum   = NULL;
double line_pos   = NULL;
double mtr_spd_l = NULL;
double mtr_spd_r = NULL;

// obstacle
double distance = 0;
double obstacle = false;

// config motors through motor shield
AF_DCMotor motorLeft(1, MOTOR12_1KHZ);
AF_DCMotor motorRight(2, MOTOR12_1KHZ);

/*
 * Reads the ir sensors.
 * 
 * reads from pin IR_PIN to IR_PIN + N_IR_SENSOrs
 * sensor reads 0 when no line is detected
 * sensor reads 1 when a line is detected
 */
void read_IR_sensors() {
  for (int sensor = 0; sensor < N_IR_SENSORS; sensor++) {
    ir_values[sensor] = (double)digitalRead(sensor + IR_PIN);
  }
}

/*
 * Reads ultrasonic sensor
 * 
 * returns distance to object.
 */
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

  // setup ir pins
  for (int pin = IR_PIN; pin < IR_PIN + N_IR_SENSORS; pin++) {
    pinMode(pin, INPUT);
  }

  // setup ultrasonic pins
  pinMode(ULTRASONIC_TX, OUTPUT);
  pinMode(ULTRASONIC_RX, INPUT);
}

void loop() {
  //object avoidance
  distance = read_ultrasonic();
  obstacle = detect_object(ULTRASONIC_THRESHOLD, distance);

  // stop if there is an obstacle
  if (obstacle) {
    mtr_spd_l = 0;
    mtr_spd_r = 0;
    Serial.println("OH shit an obsticle!!!");
  } else {
    
    //Line Follow
    read_IR_sensors();
    line_pos = get_position(ir_values, N_IR_SENSORS, &w_sum, &sum);

    // checks that line exists
    if (line_pos != -eLadNoLine) {
      // CENTER - line_pos shifts line position to be with respect to the center of the LAD Unit
      control_motors(CENTER - line_pos, STEERING_SENSITIVITY, MOTOR_SPEED, &mtr_spd_l, &mtr_spd_r);
    } else {
      Serial.println("Recalculating...");
    }

    // drive motor
    if (mtr_spd_l > 0 && mtr_spd_r > 0) {
      motorLeft.setSpeed(mtr_spd_l);
      motorRight.setSpeed(mtr_spd_r);
  
      motorLeft.run(FORWARD);
      motorRight.run(FORWARD);
    } else {
      motorLeft.run(RELEASE);
      motorRight.run(RELEASE);
    }
    
    Serial.print(mtr_spd_l);
    Serial.print("% ");
    Serial.print(mtr_spd_r);
    Serial.println("%");
  }

  delay(500);
}

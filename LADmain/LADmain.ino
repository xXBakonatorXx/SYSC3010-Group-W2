#include <AFMotor.h>
#include <Servo.h>
#include <control.h>
#include <stdint.h>

// DC motor definirtions
#define MOTOR_SPEED 60
#define STEERING_SENSITIVITY 40

// Servo definitions
#define ARM_SERVO_PORT 9
#define WRIST_SERVO_PORT 10
#define HAND_SERVO_PORT 11

// arm control definitions
#define ARM_MAX 90
#define ARM_MIN 0
#define ARM_DEFAULT 0
#define ARM_SCAN (ARM_MAX / 2)

#define WRIST_MAX 90
#define WRIST_MIN 0
#define WRIST_DEFAULT (WRIST_MAX + WRIST_MIN) / 2
#define WRIST_SCAN 90

#define HAND_MAX 180
#define HAND_MIN 0
#define HAND_DEFAULT 0
#define HAND_SCAN HAND_MAX

// IR Sensor definitions
#define N_IR_SENSORS 3
#define IR_LEFT A0
#define IR_MIDDLE A1
#define IR_RIGHT A2
#define CENTER_VALUE 2

// UltraSonic definitions
#define ULTRASONIC_THRESHOLD 10
#define ULTRASONIC_PULSE_PIN 2
#define ULTRASONIC_ECHO_PIN 3

AF_DCMotor motorLeft(3, MOTOR34_1KHZ);
AF_DCMotor motorRight(4, MOTOR34_1KHZ);

Servo armServ;
Servo wristServ;
Servo handServ;

uint16_t serial_input;
bool ir_values[N_IR_SENSORS];
bool obstacle;
double line_position;
double motor_speed_left;
double motor_speed_right;
int arm_position;
int wrist_position;
int hand_position;
int steering_factor;

double dist;

double read_ultrasonic() {
  // sends and receives a pulse from the Ultrasonic sensor
  // returns the objects distance
  
  digitalWrite(ULTRASONIC_PULSE_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(ULTRASONIC_PULSE_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(ULTRASONIC_PULSE_PIN, LOW);

  return pulseIn(ULTRASONIC_ECHO_PIN, HIGH) * 0.034 / 2;
}

uint16_t navigate(uint16_t return_code){
  //drives forward and follows the line
  
  // check for obstacle
  dist = (double) read_ultrasonic();
  obstacle = detect_object((double) ULTRASONIC_THRESHOLD, (double) dist);
  obstacle = 0;
  if (!obstacle) {
    // line follow 
    // read sensors
    ir_values[0] = (bool)(analogRead(A0) > 35);
    ir_values[1] = (bool)(analogRead(A1) > 35);
    ir_values[2] = (bool)(analogRead(A2) > 35);    

    // get line position
    line_position = (double) get_position(ir_values, (int) N_IR_SENSORS);
    if ((line_position != (double) -eLadNoLine) && (line_position != (double) - eLadAllLine)) {  // if lad is on a line
      // adjust steering factor
      control_motors((double)(CENTER_VALUE - line_position), STEERING_SENSITIVITY, (double)MOTOR_SPEED, &motor_speed_left, &motor_speed_right);
      
      // Drive motors    
      motorLeft.setSpeed(motor_speed_left);
      motorRight.setSpeed(motor_speed_right);
  
      motorLeft.run(FORWARD);
      motorRight.run(FORWARD);
    } else if ((line_position == (double) -eLadNoLine) && (line_position != (double) -eLadAllLine)){
      // find line again. (back up??)
      turn_around();
      motorLeft.run(RELEASE);
      motorRight.run(RELEASE);
    } else if ((line_position != (double) -eLadNoLine) && (line_position == (double) -eLadAllLine)) {
      return_code |= (uint16_t) LAD_SCAN_QR;
    }
  } else {
    motorLeft.run(RELEASE);
    motorRight.run(RELEASE);
  }
  return return_code;
}

void turn_left() {
  // turn left until line is detected again

  // check obstacle
  if (!obstacle) {
    // turn left
    motorLeft.run(RELEASE);
    motorRight.run(FORWARD);
  } else {
    motorLeft.run(RELEASE);
    motorRight.run(RELEASE);
  }
}

void turn_right() {
  // turn right until line is detected

  // check obstacle
  if (!obstacle) {
    // turn right
    motorLeft.run(FORWARD);
    motorRight.run(RELEASE);
  } else {
    motorLeft.run(RELEASE);
    motorRight.run(RELEASE);
  }
}

void turn_around(){
  return;
}

uint16_t control_arm(int* angle, uint16_t up, uint16_t down, uint16_t input) {
  static int deg = 5;
  // move arm component up or down
  if (input & up) {
    *angle = *angle + deg;
    return up;
  } else if (input & down) {
    *angle = *angle - deg;
    return down;
  }
}

void arm2position(uint16_t arm_position, uint16_t wrist_position, uint16_t hand_position) {
  armServ.write(arm_position);
  wristServ.write(wrist_position);
  handServ.write(hand_position);
}

int read_serial() {
  return (uint16_t) Serial.readStringUntil('\n').toInt();
}

uint16_t decode_manual(uint16_t return_code) {
  
  // decode driving
  if (serial_input & (uint16_t) DRV_FORWARD) {
    
    if (serial_input & (uint16_t) DRV_TURN_LEFT) {
      turn_left();
      return_code |= (uint16_t)(DRV_TURN_LEFT);
      
    } else if (serial_input & (uint16_t) DRV_TURN_RIGHT) {
      turn_right();
      return_code |= (uint16_t)(DRV_TURN_RIGHT);
      
    } else if (serial_input & ~((uint16_t) DRV_TURN_LEFT | (uint16_t) DRV_TURN_RIGHT)) {
      
      return_code |= (uint16_t)navigate(return_code);
      
    } else {
      turn_around();      
    }
    return_code |= (uint16_t)(DRV_FORWARD);
  } else if (serial_input & ~DRV_FORWARD) {
    // Drive motors stop
    motorLeft.run(RELEASE);
    motorRight.run(RELEASE);
  }

  // decode arm movement
  return_code |= control_arm(&arm_position, MOV_ARM_UP, MOV_ARM_DOWN, serial_input);
  return_code |= control_arm(&wrist_position, MOV_WRIST_UP, MOV_WRIST_DOWN, serial_input);
  return_code |= control_arm(&hand_position, MOV_HAND_OPEN, MOV_HAND_CLOSE, serial_input);

  // move arm
  armServ.write(arm_position);
  wristServ.write(wrist_position);
  handServ.write(hand_position);
}

uint16_t decode_automatic(uint16_t return_code) { 
  // decode drive
  if (serial_input & LAD_DRIVE) {
   
    if (serial_input & LAD_DIRECTION) {
      // turn around
      turn_around();
      return_code |= (uint16_t)(LAD_DIRECTION);
      
    } else {
      // continue straigh (ie line follow)
      return_code |= navigate(return_code);
    }
    
    return_code |= (uint16_t)(LAD_DRIVE);
  } else if (serial_input & LAD_TURN) {
  
    if (serial_input & LAD_DIRECTION) {
      // turn right
      turn_right();
      return_code |= (uint16_t)(LAD_DIRECTION);
      
    } else {
      // turn left
      turn_left();
    }
    
    return_code |= (uint16_t)(LAD_TURN);
    
  } else if (serial_input & LAD_NO_LINE) {
    // recover line
    motorLeft.run(RELEASE);
    motorRight.run(RELEASE);
    return_code |= (uint16_t)(LAD_NO_LINE);
  }
   
}

uint16_t decode_serial() {
  uint16_t return_code = 0;
  
  if (serial_input & (uint16_t) OP_MANUAL) {
    // decode manual codes
    return_code = decode_manual(OP_MANUAL);
    
  } else if (serial_input & (uint16_t) OP_AUTOMATIC) {
    // decode auto codes
    return_code = decode_automatic(OP_AUTOMATIC);
    
  } else {
    // do nothing
    motorLeft.run(RELEASE);
    motorRight.run(RELEASE);
  }
  return return_code;
}

void setup() {
  // put your setup code here, to run once:

  serial_input = 0;
  obstacle = 0;
  line_position = (double) CENTER_VALUE;
  motor_speed_left = (double) MOTOR_SPEED;
  motor_speed_right = (double) MOTOR_SPEED;
  arm_position = (int) ARM_DEFAULT;
  wrist_position = (int) WRIST_DEFAULT;
  hand_position = (int) HAND_DEFAULT;

  // set up dc motors;
  motorLeft.run(RELEASE);
  motorRight.run(RELEASE);

  motorLeft.setSpeed(MOTOR_SPEED);
  motorRight.setSpeed(MOTOR_SPEED);

  // set up servo motors
  armServ.attach(ARM_SERVO_PORT);
  wristServ.attach(WRIST_SERVO_PORT);
  handServ.attach(HAND_SERVO_PORT);

  arm2position(ARM_DEFAULT, WRIST_DEFAULT, HAND_DEFAULT);

  // set up ir sensors 
  pinMode(IR_LEFT, INPUT);
  pinMode(IR_MIDDLE, INPUT);
  pinMode(IR_RIGHT, INPUT);

  // set up ultrasonic sensor
  pinMode(ULTRASONIC_PULSE_PIN, OUTPUT);
  pinMode(ULTRASONIC_ECHO_PIN, INPUT);

  //setup Serial
  Serial.begin(9600);
}

void loop() { 
  // put your main code here, to run repeatedly:

  if (Serial.available()) {

    // read serial communication
    serial_input = (uint16_t) read_serial();
  }

  // decode, execute, and send back opcode
  Serial.println( decode_serial() );  
}

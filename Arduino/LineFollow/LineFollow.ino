#include <PID_v1.h>
#include <AFMotor.h>
#include <control.h>

#define PIN0 2
#define PIN1 3
#define PIN2 4
#define PIN3 5
#define PIN4 6

#define SPEED 75
#define FACTOR 10
#define CENTER 3

// IR sensor values
int val0  = 0;
int val1  = 0;
int val2  = 0;
int val3  = 0;
int val4  = 0;

int dir = 0;

// line position
double w_sum = 0;
double sum   = 0;
double  avg   = 0;
double  pos   = 0;
double motor_l = 0;
double motor_r = 0;

//PID Params
double setpoint;
double input;
double output;
double Kp=1, Ki=0, Kd=0;

// config motors through motor shield
AF_DCMotor motor1(1, MOTOR12_1KHZ);
AF_DCMotor motor2(2, MOTOR12_1KHZ);

// setup pid controller
/*PID ladPID(&input, &output, &setpoint, Kp, Ki, Kd, DIRECT);*/

void setup() {
  Serial.begin(9600);

  // the value pid adjusts towards
  setpoint = 0;

  //setup ir pins
  pinMode(PIN0, INPUT);
  pinMode(PIN1, INPUT);
  pinMode(PIN2, INPUT);
  pinMode(PIN3, INPUT);
  pinMode(PIN4, INPUT);

  //setup pid
  /*ladPID.SetMode(AUTOMATIC);
  ladPID.SetTunings(Kp, Ki, Kp);*/
}

void loop() {
  // read ir sensors. 1 while no object, 0 while obeject (1 when line is underneath)
  val0  = (int)digitalRead(PIN0);
  val1  = (int)digitalRead(PIN1);
  val2  = (int)digitalRead(PIN2);
  val3  = (int)digitalRead(PIN3);
  val4  = (int)digitalRead(PIN4);

  // calculates position of line under the sensors
  w_sum = (double)(val0 * 1.0 + val1 * 2.0 + val2 * 3.0 + val3 * 4.0 + val4 * 5.0);
  sum   = (double)(val0 + val1 + val2 + val3 + val4);

  if (sum == 0) {
    sum = -4;
  }
  
  avg   = (double)(w_sum / sum);

  //pid work
  
  output = CENTER - avg;
  control(output, FACTOR, SPEED, &motor_l, &motor_r);
  
  /*ladPID.Compute();*/

  Serial.print(motor_l);
  Serial.println(motor_r);

  // drive wheels
  

  //delay(1000);
}

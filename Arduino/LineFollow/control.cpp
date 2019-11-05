#include "control.h"
#include <math.h>

void control(double pid_output, double factor, double speed, double* motor_left, double* motor_right) {
    int distance2axel = 3;

    double angle  = (double) sin(pid_output / distance2axel);
    *motor_left   = (double) speed - factor * sin(angle);
    *motor_right  = (double) speed - factor * sin(angle);
}

double get_postion(double* IR_data_l) {
    double w_sum, sum;

    for (int i = 0; i < sizeof(IR_data_l); i++) {
        w_sum += IR_data_l[i] * (i + 1);
        sum   += IR_data_l[i];
    }

    return w_sum / sum;
}
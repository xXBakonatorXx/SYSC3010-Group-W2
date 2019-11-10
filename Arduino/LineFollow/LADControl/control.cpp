#include "control.h"

void control(double pid_output, double factor, double speed, double* motor_left, double* motor_right) {
	// adjust wheel power to steer toward line
	*motor_left = (double)speed - factor * pid_output;
	*motor_right = (double)speed + factor * pid_output;
}

double get_position(int values[], int n_sensors, double* weighted_sum, double* sum) {
	for (int sensor = 0; sensor < n_sensors; sensor++) {
		*weighted_sum += values[sensor] * (sensor + 1);
		*sum += values[sensor];
	}

	return *weighted_sum / *sum;
}
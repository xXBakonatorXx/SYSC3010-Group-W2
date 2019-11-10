void control_motors(double pid_output, double factor, double speed, double* motor_left, double* motor_right);
double get_position(int values[], int n_sensors, double* weighted_sum, double* sum);
bool detect_object(double threshold, double distance);
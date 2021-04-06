#include "rcProjPkg/joystickProcessing.h"

SensorProcessing::SensorProcessing(ros::NodeHandle node_handle) : node_handle(node_handle){
    sensor_sub = node_handle.subscribe(DATA_TRANSFER_TOPIC, MSG_BUFFER_SIZE, &SensorProcessing::sensor_input_callback, this);
    
    pub_to_pi = node_handle.advertise<rcProjPkg::motor_controls_msg>(CONTROLS_TO_PI_TOPIC, MSG_BUFFER_SIZE);

}

// function maps the potentiometer values ranging 0-1023 (10bit arduino ADC resolution) to a desired PWM range for RPI to handle 0-100
int map(double x, double in_min, double in_max, double out_min, double out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void SensorProcessing::sensor_input_callback(rcProjPkg::data_msg data){
    rcProjPkg::motor_controls_msg mapped_obj_msg;
   
    double processedX = (data.x*-1);
    // invert because hardware is backwards 
    double processedY = (data.y);
    std::cout << "Working with data: " << "X: " << processedX << " Y: " << processedY << std::endl;


    /* 
        would use mapping for analog single joystick (not built in)
        -50 here to get a -50 --> 0 --> 50 axis in both x and y
        int mapX = map(processedX, 0, 2, 0, 100) - 50;
        int mapY = map(processedY, 0, 2, 0, 100) - 50;

        atan2: principal - quadrant value in degrees
        +360 %360 makes negative angle values between 0-180 (what atan2 outputs for quadrants 3&4 into 0-360 range)
    */
   
    int angle = fmod(((atan2(processedY,processedX) * 180 / M_PI)+360), 360);
    double magnitude = sqrt(pow(processedX,2) + pow(processedY,2));
    // IMPORTANT: NEEDS TO BE A FLOAT ANGLE AND MAGNITUDE OTHERWISE ROS MSG WILL GIVE ERROR md5sum mismatch
    std::cout << "Magnitude: " << magnitude << std::endl;

    int mappedMag = map(magnitude, 0, 1.25, 0, 100);

    mapped_obj_msg.angle = angle;
    mapped_obj_msg.magnitude = mappedMag;
    
    std::cout << "Results: " << "ANGLE: " << angle << " MAG: " << mappedMag << std::endl;

    pub_to_pi.publish(mapped_obj_msg);
}


int main(int argc, char ** argv){
    ros::init(argc, argv, "data_processor"); // initialize the node
    ros::NodeHandle node_handle;
    SensorProcessing data = SensorProcessing(node_handle);
    std::cout<<"Processing Node Initiated"<<std::endl;
    ros::spin();
}
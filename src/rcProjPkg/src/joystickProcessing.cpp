
#include "rcProjPkg/joystickProcessing.h"

SensorProcessing::SensorProcessing(ros::NodeHandle node_handle) : node_handle(node_handle){
    sensor_sub = node_handle.subscribe(DATA_TRANSFER_TOPIC, MSG_BUFFER_SIZE, &SensorProcessing::sensor_input_callback, this);
    
    pub_to_pi = node_handle.advertise<rcProjPkg::motor_controls_msg>(CONTROLS_TO_PI_TOPIC, 10);

}

// function maps the potentiometer values ranging 0-1023 (10bit arduino ADC resolution) to a desired PWM range for RPI to handle 0-100
int map(int x, int in_min, int in_max, int out_min, int out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void SensorProcessing::sensor_input_callback(rcProjPkg::data_msg data){
    rcProjPkg::motor_controls_msg mapped_obj_msg;
    std::cout << "Received data: " << "X: " << data.x << " Y: " << data.y << std::endl;

    //invert because hardware is backwards 
    int invertY = map(data.y, 0, 1023, 1023, 0);


    // -50 here to get a -50 --> 0 --> 50 axis in both x and y
    int mapX = map(data.x, 0, 1023, 0, 100) - 50;
    int mapY = map(data.y, 0, 1023, 0, 100) - 50;

    // atan2: principal - quadrant value in degrees
    // +360 %360 makes negative angle values between 0-180 (what atan2 outputs for quadrants 3&4 into 0-360 range)
    double angle = fmod(((atan2(mapY,mapX) * 180 / M_PI)+360), 360);
    double magnitude = sqrt(pow(mapX,2) + pow(mapY,2));
    mapped_obj_msg.angle = angle;
    mapped_obj_msg.magnitude = magnitude;

    std::cout << "Mapped data: " << "ANGLE: " << angle << " MAG: " << magnitude << std::endl;

    pub_to_pi.publish(mapped_obj_msg);
}


int main(int argc, char ** argv){
    ros::init(argc, argv, "data_processor"); // initialize the node
    ros::NodeHandle node_handle;
    SensorProcessing data = SensorProcessing(node_handle);
    std::cout<<"Processing Node Initiated"<<std::endl;
    ros::spin();

}
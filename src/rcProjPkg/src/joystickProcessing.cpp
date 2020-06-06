
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

    int mapX = map(data.x, 0, 1023, 0, 100);
    int mapY = map(data.y, 0, 1023, 0, 100);

    mapped_obj_msg.mappedX = mapX;
    mapped_obj_msg.mappedY = mapY;
    
    std::cout << "Mapped data: " << "X: " << mapX << " Y: " << mapY << std::endl;

    pub_to_pi.publish(mapped_obj_msg);
}


int main(int argc, char ** argv){
    ros::init(argc, argv, "data_processor"); // initialize the node
    ros::NodeHandle node_handle;
    SensorProcessing data = SensorProcessing(node_handle);
    std::cout<<"Processing Node Initiated"<<std::endl;
    ros::spin();

}
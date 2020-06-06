
#include <wiringPi.h>
#include "rcProjPkg/motorControls.h"


// constructor
motorControlClass::motorControlClass(ros::NodeHandle node_handle) : node_handle(node_handle){
    motor_sub = node_handle.subscribe(CONTROLS_TO_PI_TOPIC, MSG_BUFFER_SIZE, &motorControlClass::motor_control_callback, this);
}


void motorControlClass::motor_control_callback(rcProjPkg::motor_controls_msg motorMsg){
    std::cout << "Received data: " << "X: " << motorMsg.mappedX << " Y: " << motorMsg.mappedY << std::endl;
}


int main(int argc, char ** argv){
    ros::init(argc, argv, "motor_controls"); // initialize the node
    ros::NodeHandle node_handle;
    motorControlClass controls = motorControlClass(node_handle);
    std::cout<<"Motor Controls Node Initiated"<<std::endl;
    ros::spin();

}
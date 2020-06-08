
#include "rcProjPkg/motorControls.h"

#define left_mterminal_1 25
#define left_mterminal_2 8
#define right_mterminal_1 7
#define right_mterminal_2 1
#define left_pwm 12
#define right_pwm 13

// void stop(){
//     digitalWrite(left_mterminal_1, 0);
//     digitalWrite(left_mterminal_2, 0);
//     digitalWrite(right_mterminal_1, 0);
//     digitalWrite(right_mterminal_2, 0);
// }


// constructor
motorControlClass::motorControlClass(ros::NodeHandle node_handle) : node_handle(node_handle){
    motor_sub = node_handle.subscribe(CONTROLS_TO_PI_TOPIC, MSG_BUFFER_SIZE, &motorControlClass::motor_control_callback, this);
}


void motorControlClass::motor_control_callback(rcProjPkg::motor_controls_msg motorMsg){
// #ifdef __arm__

    // ROS_INFO("GPIO has been set as OUTPUT.");
    // ROS_INFO("Set GPIO HIGH");
    // ros::Duration(1.0).sleep();
    // ROS_INFO("Set GPIO LOW");
    // ros::Duration(1.0).sleep();

// #else

    // std::cout << "Received data but ON X86 NOT ARM --> RUN THE NODE ON ARM" << std::endl;

// #endif
    
    std::cout << "Received data: " << "ANGLE: " << motorMsg.angle << " MAGNITUDE: " << motorMsg.magnitude << std::endl;
}


int main(int argc, char ** argv){
    ros::init(argc, argv, "motor_controls"); // initialize the node
    ros::NodeHandle node_handle;
    motorControlClass controls = motorControlClass(node_handle);
    std::cout<<"Motor Controls Node Initiated"<<std::endl;
    
    wiringPiSetupGpio();
    pinMode(left_mterminal_1, OUTPUT);
    pinMode(left_mterminal_2, OUTPUT);
    pinMode(right_mterminal_1, OUTPUT);
    pinMode(right_mterminal_2, OUTPUT);


    ros::spin();

}
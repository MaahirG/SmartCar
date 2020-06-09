
#include "rcProjPkg/motorControls.h"

#define left_mterminal_1 25
#define left_mterminal_2 8
#define right_mterminal_1 7 //right motor
#define right_mterminal_2 1 //right motor 
#define left_pwm 12 //green
#define right_pwm 13 //black

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
    if(motorMsg.magnitude > 20 && motorMsg.magnitude < 40){
        ROS_INFO("MOTORS AT 50");
        softPwmWrite(left_pwm, 50);
        softPwmWrite(right_pwm, 50);
    } else if(motorMsg.magnitude >= 40){
        ROS_INFO("MOTORS AT 100");
        softPwmWrite(left_pwm, 100);
        softPwmWrite(right_pwm, 100);
    } else if(motorMsg.magnitude <= 5){
        ROS_INFO("MOTORS AT 0");
        softPwmWrite(left_pwm, 0);
        softPwmWrite(right_pwm, 0);
    } else {
        ROS_INFO("MOTORS AT 25");
        softPwmWrite(left_pwm, 25);
        softPwmWrite(right_pwm, 25);
    }

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

    softPwmCreate(right_pwm,0,100);
    softPwmCreate(left_pwm,0,100);

    digitalWrite(7, HIGH);
    digitalWrite(1, LOW);
    ros::spin();

}
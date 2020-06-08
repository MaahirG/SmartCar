#ifndef __MOTOR_CONTROLS_H__
#define __MOTOR_CONTROLS_H__

#include "cstdlib"
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "rcProjPkg/motor_controls_msg.h"
#include <math.h>
#include <wiringPi.h>
// #include <softPwm.h>


#define MSG_BUFFER_SIZE 10
#define CONTROLS_TO_PI_TOPIC "to_pi"


class motorControlClass {
    public:
        motorControlClass(ros::NodeHandle node_handle);
    
    private:
        ros::NodeHandle node_handle;
        
        ros::Subscriber motor_sub;
        
        void motor_control_callback(rcProjPkg::motor_controls_msg motorMsg);  

};


#endif
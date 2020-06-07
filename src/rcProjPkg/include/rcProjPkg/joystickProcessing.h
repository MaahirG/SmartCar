#ifndef __JOY_STICK_PROCESSING_H__
#define __JOY_STICK_PROCESSING_H__

#include "cstdlib"
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "rcProjPkg/data_msg.h"
#include "rcProjPkg/motor_controls_msg.h"
#include <math.h>

#define DATA_TRANSFER_TOPIC "from_sensor_topic"
#define MSG_BUFFER_SIZE 10
#define CONTROLS_TO_PI_TOPIC "to_pi"

class SensorProcessing {
    public:
        SensorProcessing(ros::NodeHandle node_handle);
    
    private:
        ros::NodeHandle node_handle;
        
        ros::Subscriber sensor_sub;
        
        ros::Publisher pub_to_pi;

        void sensor_input_callback(rcProjPkg::data_msg msg);  

};


#endif
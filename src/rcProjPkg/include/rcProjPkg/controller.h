#ifndef __CONTROLLER_H__
#define __CONTROLLER_H__


#include "cstdlib"
#include <ros/ros.h>
#include <sensor_msgs/Joy.h> //included package in ROS installation
#include "rcProjPkg/data_msg.h"

#define DATA_TRANSFER_TOPIC "from_sensor_topic"
#define MSG_BUFFER_SIZE 10

class Controller {
    public:
        Controller(ros::NodeHandle node_handle);
    
    private:
        ros::NodeHandle node_handle;
        
        ros::Subscriber joy_sub;
        
        ros::Publisher pub_to_processing;

        void joy_callback(const sensor_msgs::Joy::ConstPtr& joy);
};


#endif
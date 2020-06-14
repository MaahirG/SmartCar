
#include "rcProjPkg/controller.h"

Controller::Controller(ros::NodeHandle node_handle) : node_handle(node_handle){
    joy_sub = node_handle.subscribe("joy", MSG_BUFFER_SIZE, &Controller::joy_callback, this);
    
    pub_to_processing = node_handle.advertise<rcProjPkg::data_msg>(DATA_TRANSFER_TOPIC, MSG_BUFFER_SIZE); // publish controller data to processing node

}

void Controller::joy_callback(const sensor_msgs::Joy::ConstPtr& joy){
    rcProjPkg::data_msg msg;
    std::cout << "Received data: " << "X: " << joy->axes[2] << " Y: " << joy->axes[3] << std::endl;
    msg.x = joy->axes[2];
    msg.y = joy->axes[3];
    pub_to_processing.publish(msg);
}


int main(int argc, char ** argv){
    ros::init(argc, argv, "controller_node"); // initialize the node
    ros::NodeHandle node_handle;
    Controller control = Controller(node_handle);
    std::cout<<"Controller Node Initiated"<<std::endl;
    ros::spin();

}
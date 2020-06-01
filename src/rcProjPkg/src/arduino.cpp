#include "rcProjPkg/data_msg.h"
#include <ros.h>

void setup() {
    nh.initNode();
    ros::Publisher pub = node_handle.advertise<data_msg>("from_sensor_topic", 10);
}

void loop() {
    data_msg.x = analogRead(A1);
    data_msg.y = analogRead(A0);

    pub.publish(data_msg);
    delay(500);
}
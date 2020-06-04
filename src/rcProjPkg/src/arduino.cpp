#include "rcProjPkg/data_msg.h" 
#include <ros.h>

/*
README
Need to build ros_lib with: after catkin_make and source of ros package:
cd ~/Arduino/libraries
rm -rf ros_lib
rosrun rosserial_arduino make_libraries.py .
Now upload this code to arduino then:
rosrun rosserial_arduino serial_node.py _port:= /dev/ttyACM0 <-- serial port shown in arduino IDEs 
optional: _baud:=9600 (remember to change in ArduinoHardware h file inside ros_lib)
*/

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

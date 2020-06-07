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

ros::NodeHandle nh;
rcProjPkg::data_msg msg;
ros::Publisher pub("from_sensor_topic", &msg);

void setup() {
  nh.initNode();
  nh.advertise(pub);
}

void loop() {
  int x, y;
  msg.x = analogRead(A1);
  msg.y = analogRead(A0);
//   Serial.println(x);
//   Serial.println(y);
  pub.publish(&msg);
  nh.spinOnce();
  // don't actually need a delay (add a delay for slower data reading from joystick)
  // arduino doesn't like float32 in ros msgs
  // anytime added/changed a ROS msg --> re make the ros_lib (make_libraries_py .)
}
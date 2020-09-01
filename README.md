# SmartCar

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

### Prereqs
* ROS
* OpenCV
* CMake
* Host Computer and Mobile Robot Computer
* USB Controller

### How to Use:
```sh
ON HOST COMPUTER:
roscore
New terminal: rosrun rcProjPkg ____ <-- node name that needs to be run on host machine: (controllerData, joystickProcessing and vidRead)

ON MOBILE ROBOT:
gedit ~/.bashrc
Change ROS_MASTER_URI to the command centre host computer webIP address (use ifconfig)
git clone
cd SmartCar
catkin build
New terminal: rosrun rcProjPkg ____ <-- node name that needs to be run on host machine - (motorControls and vidStream)

```

### Problem
Telerobotics will be an active contributor and play hand in hand with autonomy in Industry 4.0 and general case IoT, but the infrastructure and communication channels are too complicated.

### Solution
Telerobotics simplified - The system controls a mobile robot without range barriers provided that the robot and the remote control device are connected to the Internet.

### Telerobotics' contribution in the upcoming years of transformation:
* [https://www.marketwatch.com/press-release/emerging-role-of-teleoperation-telerobotics-in-industry-40-2020-2025-analysis-2020-04-23?mod=mw_more_headlines&tesla=y]
* [https://www.engineering.com/AdvancedManufacturing/ArticleID/13099/IIoT-and-Industry-40-to-Create-Growth-in-Telerobotics-in-Manufacturing.aspx]
* [https://ieeexplore.ieee.org/document/8075288]

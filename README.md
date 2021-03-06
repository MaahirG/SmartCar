# SmartCar
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

### Navigating the Repo
* All autonomous features: Path planning, realtime fast detection with CUDA wrappers and TensorRT, mapping visualization and transformations are found in SmartCar/autonomous 
* All telerobotics code is found in SmartCar/src/rcProjPkg/src (header files are in SmartCar/src/rcProjPkg/include/rcProjPkg)

### Prereqs For Autonomous
* Python 
* TensorRT
* Jetson.GPIO
* Pygame

### Next Step
* Publish img frames (np array) to a web server to visualize movement realtime in the browser
* Docker container with GPIO, Simulation & Video interface on mobile robot

### How to Use (Autonomous):
```sh
ON MOBILE ROBOT:
cd SmartCar/autonomous/
sudo killall ibus-daemon
python autonomous.py <-- Occupancy grid simulation and realtime video stream should show up
Press enter to start planning path and watch the car move!
Note: Multiprocessing handled for updating occupancy grid/path plan visualization and realtime video stream.
```

### Prereqs For Telerobotics (Docker container coming soon)
* ROS
* OpenCV
* CMake
* Host Computer and Mobile Robot Computer
* USB Controller

### How to Use (Telerobotics):
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

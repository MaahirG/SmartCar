cmake_minimum_required(VERSION 2.8.3)
project(rcProjPkg)

SET("OpenCV_DIR" "~/opencv/opencv/build")

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  genmsg #I ADDED
  roscpp
  std_msgs
  cv_bridge
  image_transport
  OpenCV
)

################################################
## Declare ROS messages, services and actions ##
################################################

## Generate messages in the 'msg' folder
  add_message_files(
    FILES
    data_msg.msg
    motor_controls_msg.msg
  )

## Generate services in the 'srv' folder
# add_service_files(
#   FILES
#   Service1.srv
#   Service2.srv
# )

## Generate actions in the 'action' folder
# add_action_files(
#   FILES
#   Action1.action
#   Action2.action
# )

## Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   std_msgs
 )


###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations

include_directories(
 include
  ${catkin_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
)

## Declare a C++ library
# add_library(${PROJECT_NAME}
#   src/${PROJECT_NAME}/rcProjPkg.cpp
# )

## Add cmake target dependencies of the library
## as an example, code may need to be generated before libraries
## either from message generation or dynamic reconfigure
# add_dependencies(${PROJECT_NAME} ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
 
 
 add_executable(controllerData src/controller.cpp)
 add_executable(joystickProcessing src/joystickProcessing.cpp)
 add_executable(motorControls src/motorControls.cpp)
 add_executable(vidStream src/video_stream.cpp)
 add_executable(vidRead src/vid_receiver.cpp)


 add_dependencies(controllerData ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
 add_dependencies(joystickProcessing ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
 add_dependencies(motorControls ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
 add_dependencies(vidStream ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
 add_dependencies(vidRead ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})


## Specify libraries to link a library or executable target against
 
target_link_libraries(controllerData ${catkin_LIBRARIES} )
target_link_libraries(joystickProcessing ${catkin_LIBRARIES} )


# TO ALLOW USAGE ON X86 PLATFORMS TOO WHERE WIRINGPI IS NOT NEEDED
#EXECUTE_PROCESS( COMMAND uname -m COMMAND tr -d '\n' OUTPUT_VARIABLE ARCHITECTURE )

target_link_libraries(motorControls ${catkin_LIBRARIES} -lwiringPi -lrt -lpthread)

target_link_libraries(vidStream ${catkin_LIBRARIES} )
target_link_libraries(vidStream ${OpenCV_LIBRARIES} )

target_link_libraries(vidRead ${catkin_LIBRARIES} )
target_link_libraries(vidRead ${OpenCV_LIBRARIES} )

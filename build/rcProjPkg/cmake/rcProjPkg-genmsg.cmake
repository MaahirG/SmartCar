# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "rcProjPkg: 2 messages, 0 services")

set(MSG_I_FLAGS "-IrcProjPkg:/home/maahir/rcProject_ws/src/rcProjPkg/msg;-Istd_msgs:/opt/ros/kinetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(rcProjPkg_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/maahir/rcProject_ws/src/rcProjPkg/msg/data_msg.msg" NAME_WE)
add_custom_target(_rcProjPkg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "rcProjPkg" "/home/maahir/rcProject_ws/src/rcProjPkg/msg/data_msg.msg" ""
)

get_filename_component(_filename "/home/maahir/rcProject_ws/src/rcProjPkg/msg/motor_controls_msg.msg" NAME_WE)
add_custom_target(_rcProjPkg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "rcProjPkg" "/home/maahir/rcProject_ws/src/rcProjPkg/msg/motor_controls_msg.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(rcProjPkg
  "/home/maahir/rcProject_ws/src/rcProjPkg/msg/data_msg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rcProjPkg
)
_generate_msg_cpp(rcProjPkg
  "/home/maahir/rcProject_ws/src/rcProjPkg/msg/motor_controls_msg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rcProjPkg
)

### Generating Services

### Generating Module File
_generate_module_cpp(rcProjPkg
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rcProjPkg
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(rcProjPkg_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(rcProjPkg_generate_messages rcProjPkg_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/maahir/rcProject_ws/src/rcProjPkg/msg/data_msg.msg" NAME_WE)
add_dependencies(rcProjPkg_generate_messages_cpp _rcProjPkg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/maahir/rcProject_ws/src/rcProjPkg/msg/motor_controls_msg.msg" NAME_WE)
add_dependencies(rcProjPkg_generate_messages_cpp _rcProjPkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rcProjPkg_gencpp)
add_dependencies(rcProjPkg_gencpp rcProjPkg_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rcProjPkg_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(rcProjPkg
  "/home/maahir/rcProject_ws/src/rcProjPkg/msg/data_msg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rcProjPkg
)
_generate_msg_eus(rcProjPkg
  "/home/maahir/rcProject_ws/src/rcProjPkg/msg/motor_controls_msg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rcProjPkg
)

### Generating Services

### Generating Module File
_generate_module_eus(rcProjPkg
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rcProjPkg
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(rcProjPkg_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(rcProjPkg_generate_messages rcProjPkg_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/maahir/rcProject_ws/src/rcProjPkg/msg/data_msg.msg" NAME_WE)
add_dependencies(rcProjPkg_generate_messages_eus _rcProjPkg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/maahir/rcProject_ws/src/rcProjPkg/msg/motor_controls_msg.msg" NAME_WE)
add_dependencies(rcProjPkg_generate_messages_eus _rcProjPkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rcProjPkg_geneus)
add_dependencies(rcProjPkg_geneus rcProjPkg_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rcProjPkg_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(rcProjPkg
  "/home/maahir/rcProject_ws/src/rcProjPkg/msg/data_msg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rcProjPkg
)
_generate_msg_lisp(rcProjPkg
  "/home/maahir/rcProject_ws/src/rcProjPkg/msg/motor_controls_msg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rcProjPkg
)

### Generating Services

### Generating Module File
_generate_module_lisp(rcProjPkg
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rcProjPkg
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(rcProjPkg_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(rcProjPkg_generate_messages rcProjPkg_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/maahir/rcProject_ws/src/rcProjPkg/msg/data_msg.msg" NAME_WE)
add_dependencies(rcProjPkg_generate_messages_lisp _rcProjPkg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/maahir/rcProject_ws/src/rcProjPkg/msg/motor_controls_msg.msg" NAME_WE)
add_dependencies(rcProjPkg_generate_messages_lisp _rcProjPkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rcProjPkg_genlisp)
add_dependencies(rcProjPkg_genlisp rcProjPkg_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rcProjPkg_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(rcProjPkg
  "/home/maahir/rcProject_ws/src/rcProjPkg/msg/data_msg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rcProjPkg
)
_generate_msg_nodejs(rcProjPkg
  "/home/maahir/rcProject_ws/src/rcProjPkg/msg/motor_controls_msg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rcProjPkg
)

### Generating Services

### Generating Module File
_generate_module_nodejs(rcProjPkg
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rcProjPkg
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(rcProjPkg_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(rcProjPkg_generate_messages rcProjPkg_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/maahir/rcProject_ws/src/rcProjPkg/msg/data_msg.msg" NAME_WE)
add_dependencies(rcProjPkg_generate_messages_nodejs _rcProjPkg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/maahir/rcProject_ws/src/rcProjPkg/msg/motor_controls_msg.msg" NAME_WE)
add_dependencies(rcProjPkg_generate_messages_nodejs _rcProjPkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rcProjPkg_gennodejs)
add_dependencies(rcProjPkg_gennodejs rcProjPkg_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rcProjPkg_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(rcProjPkg
  "/home/maahir/rcProject_ws/src/rcProjPkg/msg/data_msg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rcProjPkg
)
_generate_msg_py(rcProjPkg
  "/home/maahir/rcProject_ws/src/rcProjPkg/msg/motor_controls_msg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rcProjPkg
)

### Generating Services

### Generating Module File
_generate_module_py(rcProjPkg
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rcProjPkg
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(rcProjPkg_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(rcProjPkg_generate_messages rcProjPkg_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/maahir/rcProject_ws/src/rcProjPkg/msg/data_msg.msg" NAME_WE)
add_dependencies(rcProjPkg_generate_messages_py _rcProjPkg_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/maahir/rcProject_ws/src/rcProjPkg/msg/motor_controls_msg.msg" NAME_WE)
add_dependencies(rcProjPkg_generate_messages_py _rcProjPkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rcProjPkg_genpy)
add_dependencies(rcProjPkg_genpy rcProjPkg_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rcProjPkg_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rcProjPkg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rcProjPkg
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(rcProjPkg_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rcProjPkg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rcProjPkg
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(rcProjPkg_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rcProjPkg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rcProjPkg
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(rcProjPkg_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rcProjPkg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rcProjPkg
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(rcProjPkg_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rcProjPkg)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rcProjPkg\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rcProjPkg
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(rcProjPkg_generate_messages_py std_msgs_generate_messages_py)
endif()

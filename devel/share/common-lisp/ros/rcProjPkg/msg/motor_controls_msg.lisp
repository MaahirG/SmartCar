; Auto-generated. Do not edit!


(cl:in-package rcProjPkg-msg)


;//! \htmlinclude motor_controls_msg.msg.html

(cl:defclass <motor_controls_msg> (roslisp-msg-protocol:ros-message)
  ((angle
    :reader angle
    :initarg :angle
    :type cl:float
    :initform 0.0)
   (magnitude
    :reader magnitude
    :initarg :magnitude
    :type cl:float
    :initform 0.0))
)

(cl:defclass motor_controls_msg (<motor_controls_msg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <motor_controls_msg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'motor_controls_msg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rcProjPkg-msg:<motor_controls_msg> is deprecated: use rcProjPkg-msg:motor_controls_msg instead.")))

(cl:ensure-generic-function 'angle-val :lambda-list '(m))
(cl:defmethod angle-val ((m <motor_controls_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rcProjPkg-msg:angle-val is deprecated.  Use rcProjPkg-msg:angle instead.")
  (angle m))

(cl:ensure-generic-function 'magnitude-val :lambda-list '(m))
(cl:defmethod magnitude-val ((m <motor_controls_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rcProjPkg-msg:magnitude-val is deprecated.  Use rcProjPkg-msg:magnitude instead.")
  (magnitude m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <motor_controls_msg>) ostream)
  "Serializes a message object of type '<motor_controls_msg>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'angle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'magnitude))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <motor_controls_msg>) istream)
  "Deserializes a message object of type '<motor_controls_msg>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angle) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'magnitude) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<motor_controls_msg>)))
  "Returns string type for a message object of type '<motor_controls_msg>"
  "rcProjPkg/motor_controls_msg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'motor_controls_msg)))
  "Returns string type for a message object of type 'motor_controls_msg"
  "rcProjPkg/motor_controls_msg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<motor_controls_msg>)))
  "Returns md5sum for a message object of type '<motor_controls_msg>"
  "ebe86334728fd6e669c7a988dbec2160")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'motor_controls_msg)))
  "Returns md5sum for a message object of type 'motor_controls_msg"
  "ebe86334728fd6e669c7a988dbec2160")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<motor_controls_msg>)))
  "Returns full string definition for message of type '<motor_controls_msg>"
  (cl:format cl:nil "float32 angle~%float32 magnitude~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'motor_controls_msg)))
  "Returns full string definition for message of type 'motor_controls_msg"
  (cl:format cl:nil "float32 angle~%float32 magnitude~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <motor_controls_msg>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <motor_controls_msg>))
  "Converts a ROS message object to a list"
  (cl:list 'motor_controls_msg
    (cl:cons ':angle (angle msg))
    (cl:cons ':magnitude (magnitude msg))
))

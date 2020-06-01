; Auto-generated. Do not edit!


(cl:in-package rcProjPkg-msg)


;//! \htmlinclude motor_controls_msg.msg.html

(cl:defclass <motor_controls_msg> (roslisp-msg-protocol:ros-message)
  ((mappedX
    :reader mappedX
    :initarg :mappedX
    :type cl:fixnum
    :initform 0)
   (mappedY
    :reader mappedY
    :initarg :mappedY
    :type cl:fixnum
    :initform 0))
)

(cl:defclass motor_controls_msg (<motor_controls_msg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <motor_controls_msg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'motor_controls_msg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rcProjPkg-msg:<motor_controls_msg> is deprecated: use rcProjPkg-msg:motor_controls_msg instead.")))

(cl:ensure-generic-function 'mappedX-val :lambda-list '(m))
(cl:defmethod mappedX-val ((m <motor_controls_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rcProjPkg-msg:mappedX-val is deprecated.  Use rcProjPkg-msg:mappedX instead.")
  (mappedX m))

(cl:ensure-generic-function 'mappedY-val :lambda-list '(m))
(cl:defmethod mappedY-val ((m <motor_controls_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rcProjPkg-msg:mappedY-val is deprecated.  Use rcProjPkg-msg:mappedY instead.")
  (mappedY m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <motor_controls_msg>) ostream)
  "Serializes a message object of type '<motor_controls_msg>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'mappedX)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'mappedY)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <motor_controls_msg>) istream)
  "Deserializes a message object of type '<motor_controls_msg>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'mappedX)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'mappedY)) (cl:read-byte istream))
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
  "7ab62d3467f3d692a3c6d6775f2d4439")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'motor_controls_msg)))
  "Returns md5sum for a message object of type 'motor_controls_msg"
  "7ab62d3467f3d692a3c6d6775f2d4439")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<motor_controls_msg>)))
  "Returns full string definition for message of type '<motor_controls_msg>"
  (cl:format cl:nil "uint8 mappedX~%uint8 mappedY~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'motor_controls_msg)))
  "Returns full string definition for message of type 'motor_controls_msg"
  (cl:format cl:nil "uint8 mappedX~%uint8 mappedY~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <motor_controls_msg>))
  (cl:+ 0
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <motor_controls_msg>))
  "Converts a ROS message object to a list"
  (cl:list 'motor_controls_msg
    (cl:cons ':mappedX (mappedX msg))
    (cl:cons ':mappedY (mappedY msg))
))

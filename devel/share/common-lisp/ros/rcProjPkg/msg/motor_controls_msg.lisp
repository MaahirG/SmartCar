; Auto-generated. Do not edit!


(cl:in-package rcProjPkg-msg)


;//! \htmlinclude motor_controls_msg.msg.html

(cl:defclass <motor_controls_msg> (roslisp-msg-protocol:ros-message)
  ((mappedX
    :reader mappedX
    :initarg :mappedX
    :type cl:float
    :initform 0.0)
   (mappedY
    :reader mappedY
    :initarg :mappedY
    :type cl:float
    :initform 0.0))
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
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'mappedX))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'mappedY))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <motor_controls_msg>) istream)
  "Deserializes a message object of type '<motor_controls_msg>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'mappedX) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'mappedY) (roslisp-utils:decode-double-float-bits bits)))
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
  "501e3fc00f088a8af5e28080c514dcc4")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'motor_controls_msg)))
  "Returns md5sum for a message object of type 'motor_controls_msg"
  "501e3fc00f088a8af5e28080c514dcc4")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<motor_controls_msg>)))
  "Returns full string definition for message of type '<motor_controls_msg>"
  (cl:format cl:nil "float64 mappedX~%float64 mappedY~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'motor_controls_msg)))
  "Returns full string definition for message of type 'motor_controls_msg"
  (cl:format cl:nil "float64 mappedX~%float64 mappedY~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <motor_controls_msg>))
  (cl:+ 0
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <motor_controls_msg>))
  "Converts a ROS message object to a list"
  (cl:list 'motor_controls_msg
    (cl:cons ':mappedX (mappedX msg))
    (cl:cons ':mappedY (mappedY msg))
))

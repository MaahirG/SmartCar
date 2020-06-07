; Auto-generated. Do not edit!


(cl:in-package rcProjPkg-msg)


;//! \htmlinclude data_msg.msg.html

(cl:defclass <data_msg> (roslisp-msg-protocol:ros-message)
  ((x
    :reader x
    :initarg :x
    :type cl:float
    :initform 0.0)
   (y
    :reader y
    :initarg :y
    :type cl:float
    :initform 0.0))
)

(cl:defclass data_msg (<data_msg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <data_msg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'data_msg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rcProjPkg-msg:<data_msg> is deprecated: use rcProjPkg-msg:data_msg instead.")))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <data_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rcProjPkg-msg:x-val is deprecated.  Use rcProjPkg-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <data_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rcProjPkg-msg:y-val is deprecated.  Use rcProjPkg-msg:y instead.")
  (y m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <data_msg>) ostream)
  "Serializes a message object of type '<data_msg>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <data_msg>) istream)
  "Deserializes a message object of type '<data_msg>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<data_msg>)))
  "Returns string type for a message object of type '<data_msg>"
  "rcProjPkg/data_msg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'data_msg)))
  "Returns string type for a message object of type 'data_msg"
  "rcProjPkg/data_msg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<data_msg>)))
  "Returns md5sum for a message object of type '<data_msg>"
  "ff8d7d66dd3e4b731ef14a45d38888b6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'data_msg)))
  "Returns md5sum for a message object of type 'data_msg"
  "ff8d7d66dd3e4b731ef14a45d38888b6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<data_msg>)))
  "Returns full string definition for message of type '<data_msg>"
  (cl:format cl:nil "float32 x~%float32 y~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'data_msg)))
  "Returns full string definition for message of type 'data_msg"
  (cl:format cl:nil "float32 x~%float32 y~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <data_msg>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <data_msg>))
  "Converts a ROS message object to a list"
  (cl:list 'data_msg
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
))

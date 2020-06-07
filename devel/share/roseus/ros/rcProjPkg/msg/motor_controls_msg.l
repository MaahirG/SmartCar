;; Auto-generated. Do not edit!


(when (boundp 'rcProjPkg::motor_controls_msg)
  (if (not (find-package "RCPROJPKG"))
    (make-package "RCPROJPKG"))
  (shadow 'motor_controls_msg (find-package "RCPROJPKG")))
(unless (find-package "RCPROJPKG::MOTOR_CONTROLS_MSG")
  (make-package "RCPROJPKG::MOTOR_CONTROLS_MSG"))

(in-package "ROS")
;;//! \htmlinclude motor_controls_msg.msg.html


(defclass rcProjPkg::motor_controls_msg
  :super ros::object
  :slots (_angle _magnitude ))

(defmethod rcProjPkg::motor_controls_msg
  (:init
   (&key
    ((:angle __angle) 0.0)
    ((:magnitude __magnitude) 0.0)
    )
   (send-super :init)
   (setq _angle (float __angle))
   (setq _magnitude (float __magnitude))
   self)
  (:angle
   (&optional __angle)
   (if __angle (setq _angle __angle)) _angle)
  (:magnitude
   (&optional __magnitude)
   (if __magnitude (setq _magnitude __magnitude)) _magnitude)
  (:serialization-length
   ()
   (+
    ;; float64 _angle
    8
    ;; float64 _magnitude
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _angle
       (sys::poke _angle (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _magnitude
       (sys::poke _magnitude (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _angle
     (setq _angle (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _magnitude
     (setq _magnitude (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get rcProjPkg::motor_controls_msg :md5sum-) "9f60d5cf267edc4256952dd2a35a600f")
(setf (get rcProjPkg::motor_controls_msg :datatype-) "rcProjPkg/motor_controls_msg")
(setf (get rcProjPkg::motor_controls_msg :definition-)
      "float64 angle
float64 magnitude
")



(provide :rcProjPkg/motor_controls_msg "9f60d5cf267edc4256952dd2a35a600f")



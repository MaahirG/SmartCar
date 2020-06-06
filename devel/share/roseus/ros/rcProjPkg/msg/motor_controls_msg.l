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
  :slots (_mappedX _mappedY ))

(defmethod rcProjPkg::motor_controls_msg
  (:init
   (&key
    ((:mappedX __mappedX) 0.0)
    ((:mappedY __mappedY) 0.0)
    )
   (send-super :init)
   (setq _mappedX (float __mappedX))
   (setq _mappedY (float __mappedY))
   self)
  (:mappedX
   (&optional __mappedX)
   (if __mappedX (setq _mappedX __mappedX)) _mappedX)
  (:mappedY
   (&optional __mappedY)
   (if __mappedY (setq _mappedY __mappedY)) _mappedY)
  (:serialization-length
   ()
   (+
    ;; float64 _mappedX
    8
    ;; float64 _mappedY
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _mappedX
       (sys::poke _mappedX (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _mappedY
       (sys::poke _mappedY (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _mappedX
     (setq _mappedX (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _mappedY
     (setq _mappedY (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get rcProjPkg::motor_controls_msg :md5sum-) "501e3fc00f088a8af5e28080c514dcc4")
(setf (get rcProjPkg::motor_controls_msg :datatype-) "rcProjPkg/motor_controls_msg")
(setf (get rcProjPkg::motor_controls_msg :definition-)
      "float64 mappedX
float64 mappedY
")



(provide :rcProjPkg/motor_controls_msg "501e3fc00f088a8af5e28080c514dcc4")



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
    ((:mappedX __mappedX) 0)
    ((:mappedY __mappedY) 0)
    )
   (send-super :init)
   (setq _mappedX (round __mappedX))
   (setq _mappedY (round __mappedY))
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
    ;; uint8 _mappedX
    1
    ;; uint8 _mappedY
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _mappedX
       (write-byte _mappedX s)
     ;; uint8 _mappedY
       (write-byte _mappedY s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _mappedX
     (setq _mappedX (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _mappedY
     (setq _mappedY (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get rcProjPkg::motor_controls_msg :md5sum-) "7ab62d3467f3d692a3c6d6775f2d4439")
(setf (get rcProjPkg::motor_controls_msg :datatype-) "rcProjPkg/motor_controls_msg")
(setf (get rcProjPkg::motor_controls_msg :definition-)
      "uint8 mappedX
uint8 mappedY
")



(provide :rcProjPkg/motor_controls_msg "7ab62d3467f3d692a3c6d6775f2d4439")



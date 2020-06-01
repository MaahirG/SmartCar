
(cl:in-package :asdf)

(defsystem "rcProjPkg-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "data_msg" :depends-on ("_package_data_msg"))
    (:file "_package_data_msg" :depends-on ("_package"))
    (:file "motor_controls_msg" :depends-on ("_package_motor_controls_msg"))
    (:file "_package_motor_controls_msg" :depends-on ("_package"))
  ))
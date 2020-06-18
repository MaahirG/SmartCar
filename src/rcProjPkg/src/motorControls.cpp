
#include "rcProjPkg/motorControls.h"

#define left_mterminal_1 25 // in4 left motor red terminal (if high = fwd)
#define left_mterminal_2 8 // in3 left motor black
#define right_mterminal_1 7 // in2 right motor red terminal (if high = fwd)
#define right_mterminal_2 1 // in1 right motor black
#define left_pwm 13 //black
#define right_pwm 12 //green

int globalSpeed = 0;
double percent = 0.3;
// constructor
motorControlClass::motorControlClass(ros::NodeHandle node_handle) : node_handle(node_handle){
    motor_sub = node_handle.subscribe(CONTROLS_TO_PI_TOPIC, MSG_BUFFER_SIZE, &motorControlClass::motor_control_callback, this);
}

void straight(){
    digitalWrite(left_mterminal_1, HIGH);
    digitalWrite(left_mterminal_2, LOW);
    digitalWrite(right_mterminal_1, HIGH);
    digitalWrite(right_mterminal_2, LOW);
}

void back(){
    digitalWrite(left_mterminal_1, LOW);
    digitalWrite(left_mterminal_2, HIGH);
    digitalWrite(right_mterminal_1, LOW);
    digitalWrite(right_mterminal_2, HIGH);
}

void left(){
    digitalWrite(left_mterminal_1, LOW);    //left side goes backwards
    digitalWrite(left_mterminal_2, HIGH);
    digitalWrite(right_mterminal_1, HIGH);  //right side goes forwards
    digitalWrite(right_mterminal_2, LOW);
}

void right(){
    digitalWrite(left_mterminal_1, HIGH);    //left side goes forwards
    digitalWrite(left_mterminal_2, LOW);
    digitalWrite(right_mterminal_1, LOW);  //right side goes backwards
    digitalWrite(right_mterminal_2, HIGH);
}

void stop(){
    digitalWrite(left_mterminal_1, LOW);    //left side goes forwards
    digitalWrite(left_mterminal_2, LOW);
    digitalWrite(right_mterminal_1, LOW);  //right side goes backwards
    digitalWrite(right_mterminal_2, LOW);
}

void slight_fwd_right(){
    digitalWrite(left_mterminal_1, HIGH);
    digitalWrite(left_mterminal_2, LOW);
    digitalWrite(right_mterminal_1, HIGH);
    digitalWrite(right_mterminal_2, LOW);
    double temp = percent*globalSpeed;
    softPwmWrite(left_pwm, globalSpeed);
    softPwmWrite(right_pwm, temp);
    std::cout<< temp << std::endl;
    std::cout<< globalSpeed << std::endl;
}

void slight_fwd_left(){
    digitalWrite(left_mterminal_1, HIGH);
    digitalWrite(left_mterminal_2, LOW);
    digitalWrite(right_mterminal_1, HIGH);
    digitalWrite(right_mterminal_2, LOW);
    double temp = percent*globalSpeed;
    softPwmWrite(left_pwm, temp);
    softPwmWrite(right_pwm, globalSpeed);
    std::cout<< temp << std::endl;
    std::cout<< globalSpeed << std::endl;
}

void slight_bck_left(){
    digitalWrite(left_mterminal_1, LOW);
    digitalWrite(left_mterminal_2, HIGH);
    digitalWrite(right_mterminal_1, LOW);
    digitalWrite(right_mterminal_2, HIGH);
    double temp = percent*globalSpeed;
    softPwmWrite(left_pwm, temp);
    softPwmWrite(right_pwm, globalSpeed);
    std::cout<< temp << std::endl;
    std::cout<< globalSpeed << std::endl;

}

void slight_bck_right(){
    digitalWrite(left_mterminal_1, LOW);
    digitalWrite(left_mterminal_2, HIGH);
    digitalWrite(right_mterminal_1, LOW);
    digitalWrite(right_mterminal_2, HIGH);
    double temp = percent*globalSpeed;
    softPwmWrite(left_pwm, globalSpeed);
    softPwmWrite(right_pwm, temp);
    std::cout<< temp << std::endl;
    std::cout<< globalSpeed << std::endl;
}

void motorControlClass::motor_control_callback(rcProjPkg::motor_controls_msg motorMsg){
// #ifdef __arm__
    if(motorMsg.magnitude >= 75){
        ROS_INFO("MOTORS AT 100");
        softPwmWrite(left_pwm, 100);
        softPwmWrite(right_pwm, 100);
        globalSpeed = 100;
    } else if(motorMsg.magnitude >= 60 && motorMsg.magnitude < 75){
        ROS_INFO("MOTORS AT 80");
        softPwmWrite(left_pwm, 80);
        softPwmWrite(right_pwm, 80);
        globalSpeed = 80;
    } else if(motorMsg.magnitude >= 45 && motorMsg.magnitude < 60){
        ROS_INFO("MOTORS AT 70");
        softPwmWrite(left_pwm, 70);
        softPwmWrite(right_pwm, 70);
        globalSpeed = 70;
    } else if(motorMsg.magnitude >= 20 && motorMsg.magnitude < 45){
        ROS_INFO("MOTORS AT 60");
        softPwmWrite(left_pwm, 60);
        softPwmWrite(right_pwm, 60);
        globalSpeed = 60;
    } else if(motorMsg.magnitude >= 5 && motorMsg.magnitude < 20){
        ROS_INFO("MOTORS AT 45");
        softPwmWrite(left_pwm, 45);
        softPwmWrite(right_pwm, 45);
        globalSpeed = 45;
    } else {
        ROS_INFO("MOTORS OFF");
        softPwmWrite(left_pwm, 0);
        softPwmWrite(right_pwm, 0);
        globalSpeed = 0;
    }

    if(motorMsg.angle <= 15 || motorMsg.angle >= 345){
        ROS_INFO("RIGHT TURN");
        right();
    } else if(motorMsg.angle > 15 && motorMsg.angle < 75){
        ROS_INFO("SLIGHT FWD RIGHT");
        slight_fwd_right();
    } else if(motorMsg.angle <= 105 && motorMsg.angle >= 75){
        ROS_INFO("FORWARD");
        straight();
    } else if (motorMsg.angle >105 && motorMsg.angle < 165){
        ROS_INFO("SLIGHT FWD LEFT");
        slight_fwd_left();
    } else if(motorMsg.angle <= 195 && motorMsg.angle >= 165){
        ROS_INFO("LEFT TURN");
        left();
    } else if (motorMsg.angle > 195 && motorMsg.angle < 255) {
        ROS_INFO("SLIGHT BCK LEFT");
        slight_bck_left();
    } else if(motorMsg.angle <= 285 && motorMsg.angle >= 255){
        ROS_INFO("BACKWARD");
        back();
    } else if(motorMsg.angle > 285 && motorMsg.angle < 345){
        ROS_INFO("SLIGHT BCK RIGHT");
        slight_bck_right();
    } else {
        ROS_INFO("MIDDLE GROUND");
    }

// #else

    // std::cout << "Received data but ON X86 NOT ARM --> RUN THE NODE ON ARM" << std::endl;

// #endif
    
    std::cout << "Received data: " << "ANGLE: " << motorMsg.angle << " MAGNITUDE: " << motorMsg.magnitude << std::endl;
}


int main(int argc, char ** argv){
    ros::init(argc, argv, "motor_controls"); // initialize the node
    ros::NodeHandle node_handle;
    motorControlClass controls = motorControlClass(node_handle);
    std::cout<<"Motor Controls Node Initiated"<<std::endl;
    
    wiringPiSetupGpio();
    pinMode(left_mterminal_1, OUTPUT);
    pinMode(left_mterminal_2, OUTPUT);
    pinMode(right_mterminal_1, OUTPUT);
    pinMode(right_mterminal_2, OUTPUT);

    softPwmCreate(right_pwm,0,100);
    softPwmCreate(left_pwm,0,100);

    ros::spin();

}
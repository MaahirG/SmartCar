
"""
MODULE HANDLES ALL MOTOR FUNCTIONALITY

"""

import time
import Jetson.GPIO as GPIO

pins = {
	"ENA" : 32, #PWM
	"IN1" : 35,
	"IN2" : 37,
	"ENB" : 33,
	"IN3" : 31,
	"IN4" : 29 #PWM
}


def map(x, in_min, in_max, out_min, out_max):
  return ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def getCarAngleTo(curAngle, desiredAngle, experimentalZeroTurnTime, pins):
	angDiff = abs(curAngle - desiredAngle)
	turnTime = map(angDiff, 0, 360, 0, experimentalZeroTurnTime)
	if (desiredAngle > curAngle):
		print("ZEROTURN LEFT FOR TIME:", turnTime)
		GPIO.output(pins["IN1"],GPIO.HIGH)		# in1 & in2 are right side of car both together mean direction
		GPIO.output(pins["IN2"],GPIO.LOW)
		GPIO.output(pins["IN3"],GPIO.LOW)
		GPIO.output(pins["IN4"],GPIO.LOW)
	else:
		print("ZEROTURN RIGHT FOR TIME:", turnTime)
		GPIO.output(pins["IN1"],GPIO.LOW)
		GPIO.output(pins["IN2"],GPIO.LOW)
		GPIO.output(pins["IN3"],GPIO.LOW)
		GPIO.output(pins["IN4"],GPIO.HIGH)
	time.sleep(turnTime)
	stopCar(pins)	


def moveCar(pins):
	print("Motors Forward")
	GPIO.output(pins["IN1"],GPIO.HIGH)
	GPIO.output(pins["IN2"],GPIO.LOW)
	GPIO.output(pins["IN3"],GPIO.LOW)
	GPIO.output(pins["IN4"],GPIO.HIGH)


def stopCar(pins):
	GPIO.output(pins["IN1"],GPIO.LOW)
	GPIO.output(pins["IN2"],GPIO.LOW)
	GPIO.output(pins["IN3"],GPIO.LOW)
	GPIO.output(pins["IN4"],GPIO.LOW)
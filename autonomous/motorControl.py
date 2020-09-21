import Jetson.GPIO as GPIO
import time

# Pin Definitions
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

experimentalZeroTurnTime = 4
def getCarAngleTo(curAngle, desiredAngle, experimentalZeroTurnTime):
		angDiff = abs(curAngle - desiredAngle)
		turnTime = map(angDiff, 0, 360, 0, experimentalZeroTurnTime)

		if (desiredAngle > curAngle):
			print("ZEROTURN LEFT FOR TIME:", turnTime)
			GPIO.output(pins["IN1"],GPIO.HIGH)
			GPIO.output(pins["IN2"],GPIO.LOW)
			GPIO.output(pins["IN3"],GPIO.HIGH)
			GPIO.output(pins["IN4"],GPIO.LOW)
		else:
			print("ZEROTURN RIGHT FOR TIME:", turnTime)
			GPIO.output(pins["IN1"],GPIO.LOW)
			GPIO.output(pins["IN2"],GPIO.HIGH)
			GPIO.output(pins["IN3"],GPIO.LOW)
			GPIO.output(pins["IN4"],GPIO.HIGH)
		
		time.sleep(turnTime)
		stopCar()	


def moveCar(speed):
    print('Motors Forward at SPEED:', speed)
    GPIO.output(pins["IN1"],GPIO.HIGH)
    GPIO.output(pins["IN2"],GPIO.LOW)
    GPIO.output(pins["IN3"],GPIO.LOW)
    GPIO.output(pins["IN4"],GPIO.HIGH)


def stopCar():
    GPIO.output(pins["IN1"],GPIO.LOW)
    GPIO.output(pins["IN2"],GPIO.LOW)
    GPIO.output(pins["IN3"],GPIO.LOW)
    GPIO.output(pins["IN4"],GPIO.LOW)


def main():
    pinList = []
    GPIO.setmode(GPIO.BOARD)
    
    for key in pins.keys():
        pinList.append(pins[key])
    
    GPIO.setup(pinList, GPIO.OUT, initial=GPIO.LOW)

    APWM = GPIO.PWM(pins["ENA"],50) # Frequency 100 cycles per second
    BPWM = GPIO.PWM(pins["ENB"],50) # Frequency 100 cycles per second

    APWM.start(100) # Duty Cycle
    BPWM.start(100)


    # Straight Floor = 4.9
    # 360 100-0 Diff Floor = 16
    # Straight Carpet = 3.3
    # 360 100-0 Diff Carpet = 12.5


    try:
        while True:
            GPIO.output(pins["IN1"],GPIO.HIGH)
            GPIO.output(pins["IN2"],GPIO.LOW)
            GPIO.output(pins["IN3"],GPIO.LOW)
            GPIO.output(pins["IN4"],GPIO.HIGH)
            time.sleep(6)
            stop()
            # moveCar(60)
            # time.sleep(7)
            # break
            # time.sleep(1)
            # stopCar()
            # time.sleep(1)
            # getCarAngleTo(270, 180, 3)
            # time.sleep(1)


    finally:
        print("Cleanup")
        GPIO.cleanup()

if __name__ == '__main__':
    main()
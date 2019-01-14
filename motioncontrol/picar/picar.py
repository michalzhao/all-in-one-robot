#!/usr/bin/python3
# author Ingmar Stapel
# version 0.1 BETA
# date 20190113

import webiopi
from time import sleep
import getopt
import sys
GPIO = webiopi.GPIO

# initiales setzen der Beschleunigung
acceleration = 0
turnacceleration = 0
# auf der Stelle drehen = false
spotturn = "false"
	
# Here we configure the PWM settings for
# the two DC motors. It defines the two GPIO
# pins used for the input on the L298 H-Bridge,
# starts the PWM and sets the
# motors' speed initial to 0
MAXSPEED = 100
MAXSTEERSPEED = 50
motorDriveForwardPin = 6 #29
motorDriveReversePin = 5 #31
motorSteerLeftPin = 13 #33
motorSteerRightPin = 19 #35
motorDrivePWM = 20 #38
motorSteerPWM = 21 #40

#setup function is called automatically at WebIoPi startup
def setup():
	GPIO.setFunction(motorDriveForwardPin, GPIO.OUT)
	GPIO.setFunction(motorDriveReversePin, GPIO.OUT)
	GPIO.setFunction(motorSteerLeftPin, GPIO.OUT)
	GPIO.setFunction(motorSteerRightPin, GPIO.OUT)
	GPIO.setFunction(motorDrivePWM, GPIO.PWM)
	GPIO.setFunction(motorSteerPWM, GPIO.PWM)


def initiate():
	global acceleration
	global turnacceleration
	global motorDriveSpeed
	global motorSteerSpeed
	global speedstep
	global maxspeed
	global maxsteerspeed	
	global minspeed
	
	spotturn = "false"
	acceleration = 0
	turnacceleration = 0
	motorDriveSpeed = 0
	motorSteerSpeed = 0
	speedstep = 10
	maxspeed = 100
	maxsteerspeed = 50
	minspeed = 0

def reverse():
    GPIO.digitalWrite(motorDriveForwardPin, GPIO.LOW)
    GPIO.digitalWrite(motorDriveReversePin, GPIO.HIGH)
	
def forward():
    GPIO.digitalWrite(motorDriveForwardPin, GPIO.HIGH)
    GPIO.digitalWrite(motorDriveReversePin, GPIO.LOW)

def left():
    GPIO.digitalWrite(motorSteerLeftPin, GPIO.HIGH)
    GPIO.digitalWrite(motorSteerRightPin, GPIO.LOW)

def right():
    GPIO.digitalWrite(motorSteerLeftPin, GPIO.LOW)
    GPIO.digitalWrite(motorSteerRightPin, GPIO.HIGH)

def resetSteer():
	GPIO.digitalWrite(motorSteerLeftPin, GPIO.LOW)
	GPIO.digitalWrite(motorSteerRightPin, GPIO.LOW)

def resetSpeed():
	GPIO.digitalWrite(motorDriveForwardPin, GPIO.LOW)
	GPIO.digitalWrite(motorDriveReversePin, GPIO.LOW)
	
# stop the motors
def stop():
	GPIO.digitalWrite(motorDriveForwardPin, GPIO.LOW)
	GPIO.digitalWrite(motorDriveReversePin, GPIO.LOW)
	GPIO.digitalWrite(motorSteerLeftPin, GPIO.LOW)
	GPIO.digitalWrite(motorSteerRightPin, GPIO.LOW)
	# motorLspeed, motorRspeed, acceleration
	initiate()
	return 0, 0, 0

# stop the motors
def stopSteer():
	GPIO.digitalWrite(motorSteerLeftPin, GPIO.LOW)
	GPIO.digitalWrite(motorSteerRightPin, GPIO.LOW)


# This functions sets the motor speed.
def setacceleration(value):
	global motorDriveSpeed
	global motorSteerSpeed
	global acceleration
	global minspeed
	global maxspeed
	
	acceleration = acceleration + value
	
	minspeed, maxsteerspeed = getMinMaxSpeed()
	
	#Set Min and Max values for acceleration
	if(acceleration < -MAXSPEED):
		acceleration = -MAXSPEED
	
	if(acceleration > MAXSPEED):
		acceleration = MAXSPEED	
	
	if(acceleration > 0):
		# drive forward
		forward()
		motorDriveSpeed = acceleration
		print("forward: ", motorDriveSpeed)
	elif(acceleration == 0):
		# stopp motors
		motorDriveSpeed = acceleration
		motorDriveSpeed, motorSteerSpeed, acceleration = stop()
		print("stop: ", motorDriveSpeed)
	else:
		# drive backward
		reverse()
		motorDriveSpeed = (acceleration * -1)
		print("backward: ", motorDriveSpeed)
	
	motorDriveSpeed, motorSteerSpeed = check_motorspeed(motorDriveSpeed, motorSteerSpeed)
	#print("check: ", motorLspeed, motorRspeed)

# This functions sets the motor speed.
def setturnacceleration(value):
	global motorDriveSpeed
	global motorSteerSpeed
	global turnacceleration
	global minspeed
	global maxsteerspeed
	
	turnacceleration = turnacceleration + value
	
	minspeed, maxsteerspeed = getMinMaxSteerSpeed()
	
	#Set Min and Max values for acceleration
	if(turnacceleration < -MAXSTEERSPEED):
		turnacceleration = -MAXSTEERSPEED
	
	if(turnacceleration > MAXSTEERSPEED):
		turnacceleration = MAXSTEERSPEED	
	
	if(turnacceleration > 0):
		# drive forward
		left()
		motorSteerSpeed = turnacceleration
		#print("forward: ", motorLspeed, motorRspeed)
	elif(turnacceleration == 0):
		# stopp motors
		motorSteerSpeed = turnacceleration
		motorSteerSpeed, turnacceleration = stopSteer()
		#print("stop: ", motorLspeed, motorRspeed)
	else:
		# drive backward
		right()
		motorSteerSpeed = (turnacceleration * -1)
		#print("backward: ", motorLspeed, motorRspeed)
	
	motorDriveSpeed, motorSteerSpeed = check_motorspeed(motorDriveSpeed, motorSteerSpeed)	

# check the motorspeed if it is correct and in max/min range
def check_motorspeed(motorDriveSpeed, motorSteerSpeed):
	if (motorDriveSpeed < minspeed):
		motorDriveSpeed = minspeed

	if (motorDriveSpeed > maxspeed):
		motorDriveSpeed = maxspeed
		
	if (motorSteerSpeed < minspeed):
		motorSteerSpeed = minspeed

	if (motorSteerSpeed > maxspeed):
		motorSteerSpeed = maxspeed	
		
	return motorDriveSpeed, motorSteerSpeed

# Set Min Max Speed
def getMinMaxSpeed():
	minspeed = 0
	maxspeed = 100
	return minspeed, maxspeed

# Set Min Max Speed
def getMinMaxSteerSpeed():
	minspeed = 0
	maxsteerspeed = 50
	return minspeed, maxsteerspeed
	
# Get the motor speed
def getMotorSpeed():
	global motorDriveSpeed
	global motorSteerSpeed
	
	return motorDriveSpeed, motorSteerSpeed

def getMotorSpeedStep():
	return 7	

def getSteerMotorSpeedStep():
	return 50		
	
@webiopi.macro
def ButtonForward():
	fowardAcc = 0
	fowardAcc = getMotorSpeedStep()

	setacceleration(fowardAcc)
	
	motorDriveSpeed, motorSteerSpeed = getMotorSpeed()
	
	# percent calculation	
	valueDrive =  float(motorDriveSpeed)/100
		
	GPIO.pulseRatio(motorDrivePWM, valueDrive)

	
@webiopi.macro
def ButtonReverse():
	backwardAcc = 0
	backwardAcc = getMotorSpeedStep()

	setacceleration((backwardAcc*-1))
	
	motorDriveSpeed, motorSteerSpeed = getMotorSpeed()
	
	# percent calculation
	valueDrive = float(motorDriveSpeed)/100
		
	GPIO.pulseRatio(motorDrivePWM, valueDrive)
	

@webiopi.macro
def ButtonTurnLeft():
	left()
	GPIO.pulseRatio(motorSteerPWM, 0.7)	
	sleep(0.3)
	resetSteer()
	
def TurnLeft():
	left()
	GPIO.pulseRatio(motorSteerPWM, 0.7)	

def TurnRight():
	right()
	GPIO.pulseRatio(motorSteerPWM, 0.7)

@webiopi.macro	
def ButtonTurnRight():
	right()
	GPIO.pulseRatio(motorSteerPWM, 0.7)
	sleep(0.3)	
	resetSteer()

def ButtonTurnLeftOld():
	global motorSteerSpeed
	global motorDriveSpeed
	global speedstep

	steerLeftAcc = 0
	steerLeftAcc = getSteerMotorSpeedStep()

	setturnacceleration((steerLeftAcc))
	
	motorDriveSpeed, motorSteerSpeed = getMotorSpeed()
	
	# percent calculation
	valueDrive = float(motorSteerSpeed)/100
		
	GPIO.pulseRatio(motorSteerPWM, valueDrive)
	
	#print("LEFT: ",valueL,valueR,spotturn)	
@webiopi.macro
def ButtonTurnRightOld():
	global motorSteerSpeed
	global motorDriveSpeed
	global speedstep

	steerRightAcc = 0
	steerRightAcc = getSteerMotorSpeedStep()

	setturnacceleration((steerRightAcc*-1))
	
	motorDriveSpeed, motorSteerSpeed = getMotorSpeed()
	
	# percent calculation
	valueDrive = float(motorSteerSpeed)/100
		
	GPIO.pulseRatio(motorSteerPWM, valueDrive)
	
	#print("RIGHT: ",valueL,valueR, spotturn)		

@webiopi.macro
def ButtonFlashAll():
	flashAll()

@webiopi.macro
def ButtonStop():	
	stop()

def showhelp():
	print ("Usage: %s [-h] [-m] [-b] [-l] [-r] [-a]" % (sys.argv[0]))
	print ("-h --help show help")
	print ("-m --move move forward")
	print ("-b --back move backward")
	print ("-l --left turn left")
	print ("-r --right turn right")
	print ("-a --auto show demo")
	print ("Example1: ./picar -m")
	print ("Example2: sudo python3 picar.py -m")
	
	
	
def main():
	setup()
	initiate()
	argumentList = sys.argv[1:]
	#print (len(argumentList))
	unixOptions = "hmblrao:v"  
	gnuOptions = ["help", "move", "back", "left", "right", "auto"]
	
	try:  
		arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
	except getopt.error as err:  
		# output error, and return with an error code
		print (str(err))
		showhelp()
		sys.exit(2)
    
	for currentArgument, currentValue in arguments:  
		if currentArgument in ("-h", "--help"):
			showhelp()
		elif currentArgument in ("-m", "--move"):
			print ("moving forward")
			for i in range(15):
				sleep(0.1)
				ButtonForward()
			ButtonStop()
		elif currentArgument in ("-b", "--back"):
			print ("moving back")
			for i in range(15):
				sleep(0.1)
				ButtonReverse()
			ButtonStop()
		elif currentArgument in ("-l", "--left"):
			print ("turning left")
			ButtonTurnLeft()
			ButtonStop()
		elif currentArgument in ("-r", "--right"):
			print ("turning right")
			ButtonTurnRight()
			ButtonStop()
		elif currentArgument in ("-a", "--auto"):
			print ("show a demo")
			for i in range(15):
				sleep(0.1)
				ButtonForward()
			ButtonStop()
			for i in range(15):
				sleep(0.1)
				ButtonReverse()
			ButtonStop()
			for i in range(15):
				sleep(0.1)
				ButtonForward()
			ButtonStop()
			for i in range(15):
				sleep(0.1)
				ButtonReverse()
			ButtonStop()
				
				
if __name__ == "__main__":
	main()

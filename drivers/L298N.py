from gpiozero import PWMOutputDevice
from time import sleep


# Motor A, Left Side GPIO CONSTANTS
PWM_FORWARD_LEFT_PIN = 12	# IN1 - Forward Drive
PWM_REVERSE_LEFT_PIN = 13	# IN2 - Reverse Drive
# Motor B, Right Side GPIO CONSTANTS
PWM_FORWARD_RIGHT_PIN = 19	# IN1 - Forward Drive
PWM_REVERSE_RIGHT_PIN = 18	# IN2 - Reverse Drive

# Initialise objects for H-Bridge PWM pins
# Set initial duty cycle to 0 and frequency to 1000


forwardLeft = PWMOutputDevice(PWM_FORWARD_LEFT_PIN)
reverseLeft = PWMOutputDevice(PWM_REVERSE_LEFT_PIN)
forwardRight = PWMOutputDevice(PWM_FORWARD_RIGHT_PIN)
reverseRight = PWMOutputDevice(PWM_REVERSE_RIGHT_PIN)

def allStop():
	forwardLeft.value = 0
	reverseLeft.value = 0
	forwardRight.value = 0
	reverseRight.value = 0

def forwardDrive():
	forwardLeft.value = 1.0
	reverseLeft.value = 0
	forwardRight.value = 1.0
	reverseRight.value = 0

def reverseDrive():
	forwardLeft.value = 0
	reverseLeft.value = 1.0
	forwardRight.value = 0
	reverseRight.value = 1.0

def spinLeft():
	forwardLeft.value = 0
	reverseLeft.value = 1.0
	forwardRight.value = 1.0
	reverseRight.value = 0

def SpinRight():
	forwardLeft.value = 1.0
	reverseLeft.value = 0
	forwardRight.value = 0
	reverseRight.value = 1.0

def forwardTurnLeft():
	forwardLeft.value = 0.2
	reverseLeft.value = 0
	forwardRight.value = 0.8
	reverseRight.value = 0

def forwardTurnRight():
	forwardLeft.value = 0.8
	reverseLeft.value = 0
	forwardRight.value = 0.2
	reverseRight.value = 0

def reverseTurnLeft():
	forwardLeft.value = 0
	reverseLeft.value = 0.2
	forwardRight.value = 0
	reverseRight.value = 0.8

def reverseTurnRight():
	forwardLeft.value = 0
	reverseLeft.value = 0.8
	forwardRight.value = 0
	reverseRight.value = 0.2
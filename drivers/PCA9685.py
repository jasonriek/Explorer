import RPi.GPIO as GPIO
import time
from adafruit_pca9685 import PCA9685
import busio

# Setup GPIO pins for REN and LEN
REN_PIN = 17  # GPIO 17, Physical Pin 11
LEN_PIN = 27  # GPIO 27, Physical Pin 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(REN_PIN, GPIO.OUT)
GPIO.setup(LEN_PIN, GPIO.OUT)

# Set up I2C and PCA9685 for PWM control
i2c = busio.I2C(3, 2)
pca = PCA9685(i2c)
pca.frequency = 60  # Set the PWM frequency

# Function to set motor direction and speed
def set_motor_speed(rpwm, lpwm, ren, len):
    GPIO.output(REN_PIN, ren)
    GPIO.output(LEN_PIN, len)
    pca.channels[0].duty_cycle = rpwm  # Control RPWM
    pca.channels[1].duty_cycle = lpwm  # Control LPWM
    pca.channels[2].duty_cycle = rpwm  # Control RPWM
    pca.channels[3].duty_cycle = lpwm  # Control LPWM

# Example usage: Forward motion
set_motor_speed(0xFFFF, 0, GPIO.HIGH, GPIO.LOW)  # 50% speed forward

time.sleep(5)

# Reverse motion
set_motor_speed(0, 0x7FFF, GPIO.LOW, GPIO.HIGH)  # 50% speed reverse

time.sleep(5)

# Stop motor
set_motor_speed(0, 0, GPIO.LOW, GPIO.LOW)  # Stop

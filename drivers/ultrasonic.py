import RPi.GPIO as GPIO
import time

# Define the GPIO pin connected to the PING))) SIG pin (GPIO 17 in your case)
PING_PIN = 17

# Set up the GPIO
GPIO.setmode(GPIO.BCM)

def get_distance():
    # Set pin to OUTPUT mode to send the pulse
    GPIO.setup(PING_PIN, GPIO.OUT)
    
    # Send a low pulse for at least 2 microseconds to trigger the sensor
    GPIO.output(PING_PIN, GPIO.LOW)
    time.sleep(0.02)  # 20 ms delay to settle
    GPIO.output(PING_PIN, GPIO.HIGH)
    time.sleep(0.00002)  # 2 microseconds pulse
    GPIO.output(PING_PIN, GPIO.LOW)
    
    # Switch to input to listen for the echo
    GPIO.setup(PING_PIN, GPIO.IN)
    
    # Measure the time the signal takes to return
    start_time = time.time()
    
    while GPIO.input(PING_PIN) == 0:
        start_time = time.time()
        
    while GPIO.input(PING_PIN) == 1:
        end_time = time.time()

    # Calculate time duration
    duration = end_time - start_time
    
    # Calculate the distance (34300 cm/s is the speed of sound)
    distance = (duration * 34300) / 2  # Divide by 2 for the round trip
    
    return distance

try:
    while True:
        distance = get_distance()
        print(f"Distance: {distance:.2f} cm")
        time.sleep(1)  # Delay before next reading

except KeyboardInterrupt:
    print("Measurement stopped by User")

finally:
    GPIO.cleanup()

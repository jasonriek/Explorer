import RPi.GPIO as GPIO

# Set up GPIO mode globally
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering

# Helper function to control an LED
def control_led(pin, state):
    """Control the LED on the specified pin.
    
    Args:
        pin (int): GPIO pin number.
        state (bool): True to turn on, False to turn off.
    """
    GPIO.setup(pin, GPIO.OUT)  # Ensure the pin is set to output mode
    GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)

# Function to turn on the LED
def turn_on_led(pin):
    """Turn on the LED connected to the specified pin."""
    control_led(pin, True)
    print(f"LED on pin {pin} is ON")

# Function to turn off the LED
def turn_off_led(pin):
    """Turn off the LED connected to the specified pin."""
    control_led(pin, False)
    print(f"LED on pin {pin} is OFF")

# Example usage
try:
    # Define the pins for your LEDs
    led_pin_1 = 6  # GPIO 6
    led_pin_2 = 26  # Another GPIO pin for a second LED

    # Turn on the first LED
    turn_on_led(led_pin_1)

    # Turn off the first LED
    turn_off_led(led_pin_1)

    # Turn on the second LED
    turn_on_led(led_pin_2)

    # Turn off the second LED
    turn_off_led(led_pin_2)

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    # Clean up the GPIO settings
    GPIO.cleanup()

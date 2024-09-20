import RPi.GPIO as GPIO
import sys

# Set up GPIO mode globally
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering

# Helper function to control an LED
def control_led(pin, state):
    """Control the LED on the specified pin.
    
    Args:
        pin (int): GPIO pin number.
        state (bool): True to turn on, False to turn off.
    """
    pin = int(pin)
    GPIO.setup(pin, GPIO.OUT)  # Ensure the pin is set to output mode
    GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)

# Main function to parse arguments and control the LEDs
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 led_control.py <pin> <on/off>")
        sys.exit(1)

    pin = int(sys.argv[1])
    action = sys.argv[2].lower()

    if action == "on":
        control_led(pin, True)
        print(f"LED on pin {pin} is ON")
    elif action == "off":
        control_led(pin, False)
        print(f"LED on pin {pin} is OFF")
    else:
        print("Invalid action. Use 'on' or 'off'.")

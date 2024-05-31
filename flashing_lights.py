import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set up GPIO17 as an output pin
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
        time.sleep(1)  # Wait for 1 second
        GPIO.output(LED_PIN, GPIO.LOW)   # Turn off LED
        time.sleep(1)  # Wait for 1 second
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()  # Clean up GPIO settings


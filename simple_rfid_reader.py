import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522

# Set up GPIO
GPIO.setmode(GPIO.BCM)
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

# Initialize RFID reader
reader = SimpleMFRC522()

try:
    print("Place your RFID tag near the reader")

    while True:
        # Read the RFID tag
        id, text = reader.read()
        print(f"ID: {id}\nText: {text}")

        # Check the ID or text of the tag
        if id == 151042647098:  # Replace with your tag's ID
            # Turn on the LED
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("LED is on")
            time.sleep(5)  # Keep the LED on for 5 seconds
            GPIO.output(LED_PIN, GPIO.LOW)
            print("LED is off")
        else:
            print("Unknown RFID tag")

        time.sleep(1)  # Wait before the next read

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()

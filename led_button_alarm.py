import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta

# Set up GPIO
LED_PIN = 18
BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def flash_led():
    """Function to flash the LED"""
    while not GPIO.input(BUTTON_PIN):  # Continue flashing until the button is pressed
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)
    GPIO.output(LED_PIN, GPIO.LOW)  # Ensure the LED is off when the alarm is stopped

def set_alarm(duration_minutes):
    """Function to set an alarm"""
    alarm_time = datetime.now() + timedelta(minutes=duration_minutes)
    print(f"Alarm set for {alarm_time.strftime('%H:%M:%S')}")
    while datetime.now() < alarm_time:
        time.sleep(1)  # Sleep until the alarm time is reached

    print("Alarm going off!")
    flash_led()

try:
    duration = int(input("Enter alarm duration in minutes: "))
    set_alarm(duration)
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    GPIO.cleanup()

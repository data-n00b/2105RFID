import RPi.GPIO as GPIO
import time

def flash_led(pin, flashes):
    """
    Flash an LED connected to the specified GPIO pin a given number of times.

    Parameters:
    pin (int): The GPIO pin number where the LED is connected.
    flashes (int): The number of times the LED should flash.
    """
    # Set the GPIO mode to BCM
    GPIO.setmode(GPIO.BCM)
    
    # Set up the pin as an output pin
    GPIO.setup(pin, GPIO.OUT)

    try:
        for _ in range(flashes):
            GPIO.output(pin, GPIO.HIGH)  # Turn on LED
            time.sleep(1)  # Wait for 1 second
            GPIO.output(pin, GPIO.LOW)   # Turn off LED
            time.sleep(1)  # Wait for 1 second
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()  # Clean up GPIO settings

# Example usage:
if __name__ == "__main__":
    LED_PIN = 18  # Define the GPIO pin number
    FLASHES = 5   # Define the number of flashes
    flash_led(LED_PIN, FLASHES)

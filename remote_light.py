import RPi.GPIO as GPIO
import socket
import time

# Setup GPIO
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
led_state = False

# Socket setup
SERVER_IP = '0.0.0.0'  # Listen on all interfaces
SERVER_PORT = 65432

def toggle_led():
    global led_state
    led_state = not led_state
    GPIO.output(LED_PIN, led_state)

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
        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    s.listen()

    print(f"Listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            if data == b'TOGGLE':
                #toggle_led()
                flash_led(18,5)
            #elif data == b'FLASH':
                #flash_led()

GPIO.cleanup()

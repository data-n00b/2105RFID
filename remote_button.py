import RPi.GPIO as GPIO
import socket
import time

# Setup GPIO
BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Socket setup
SERVER_IP = '192.168.1.215'  # Replace with Pi2's IP address
SERVER_PORT = 65432

def button_callback(channel):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(b'TOGGLE')
            #s.sendall(b'FLASH')
    except Exception as e:
        print(f"Connection error: {e}")

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

import RPi.GPIO as GPIO
import socket

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
                toggle_led()

GPIO.cleanup()

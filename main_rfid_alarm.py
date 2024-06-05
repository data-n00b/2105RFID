import RPi.GPIO as GPIO
import socket
import time
from mfrc522 import SimpleMFRC522

# GPIO pin constants
LED_PIN = 18

# RFID reader setup
reader = SimpleMFRC522()

def setup_gpio():
    print('ALarm is ringing')
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(LED_PIN, GPIO.OUT)

def flash_led():
    """
    Flash an LED indefinitely until stopped by swiping the correct RFID tag.
    """
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)

def send_stop_signal():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.1.215", 9999))  # Replace "server_pi_ip" with the server's IP address
    client.send("STOP".encode())
    response = client.recv(1024).decode()
    print(response)
    client.close()

def read_rfid_and_stop_alarm():
    print("Waiting for RFID tag...")
    while True:
        try:
            id, text = reader.read()
            print(f"RFID tag detected with ID: {id}")
            if str(id) == 151042647098:  # Replace with your specific tag ID
                send_stop_signal()
                print("Alarm stopped by RFID")
                break
        except Exception as e:
            print(f"Error reading RFID: {e}")

if __name__ == "__main__":
    try:
        setup_gpio()
        alarm_thread = threading.Thread(target=flash_led)
        alarm_thread.start()
        read_rfid_and_stop_alarm()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

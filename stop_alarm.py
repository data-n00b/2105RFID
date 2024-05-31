import socket
import RPi.GPIO as GPIO

# GPIO pin constants
BUTTON_PIN = 17

def button_callback(channel):
    send_stop_signal()
    exit(0)

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

def send_stop_signal():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.1.215", 9999))  # Replace "server_pi_ip" with the server's IP address
    client.send("STOP".encode())
    response = client.recv(1024).decode()
    print(response)
    client.close()

if __name__ == "__main__":
    try:
        setup_gpio()
        print("Press the button to stop the alarm.")
        # Keep the script running to detect button presses
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()  # Clean up GPIO settings

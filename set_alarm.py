import time
import datetime
import socket
import threading
import RPi.GPIO as GPIO

# GPIO pin constants
LED_PIN = 18

# Global variable to control the alarm state
alarm_active = True

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

def flash_led():
    """
    Flash an LED indefinitely until stopped by a signal from the client.
    """
    global alarm_active
    while alarm_active:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
        time.sleep(0.5)  # Wait for half a second
        GPIO.output(LED_PIN, GPIO.LOW)   # Turn off LED
        time.sleep(0.5)  # Wait for half a second

def set_alarm(alarm_time):
    """
    Set an alarm on the Raspberry Pi.

    Parameters:
    alarm_time (str): The time at which the alarm should go off in 'HH:MM' format.
    """
    global alarm_active
    
    # Get the current time
    now = datetime.datetime.now()
    
    # Parse the alarm time
    alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
    alarm_today = datetime.datetime(now.year, now.month, now.day, alarm_hour, alarm_minute)
    
    # If the alarm time has already passed today, set it for tomorrow
    if alarm_today <= now:
        alarm_today += datetime.timedelta(days=1)

    print(f"Alarm is set for {alarm_today}")

    # Calculate the time difference between now and the alarm time
    time_diff = (alarm_today - now).total_seconds()
    
    # Wait until the alarm time
    time.sleep(time_diff)

    # Perform the alarm action
    print("Alarm! Time to wake up!")
    alarm_active = True
    flash_led()

def handle_client_connection(client_socket):
    global alarm_active
    while True:
        message = client_socket.recv(1024).decode()
        if message == "STOP":
            alarm_active = False
            client_socket.send("Alarm stopped".encode())
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(1)
    print("Waiting for a connection from the alarm stopper client...")
    client_socket, addr = server.accept()
    print(f"Connection established with {addr}")
    handle_client_connection(client_socket)

if __name__ == "__main__":
    try:
        setup_gpio()
        alarm_time = input("Enter the alarm time (HH:MM): ")
        
        # Start the server in a separate thread
        server_thread = threading.Thread(target=start_server)
        server_thread.start()
        
        # Set the alarm
        set_alarm(alarm_time)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()  # Clean up GPIO settings

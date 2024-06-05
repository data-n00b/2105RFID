import time
import datetime
import socket
import threading
#import I2C_LCD_driver
from RPLCD.i2c import CharLCD

# Global variable to control the alarm state
alarm_active = True

# Setup the LCD display
#lcd = I2C_LCD_driver.lcd()
lcd = CharLCD(i2c_expander = 'PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()

lcd.write_string("My Love!")

def display_message(message):
    lcd.clear()
    lcd.write_string(message, 1)

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
    if (alarm_today - now).total_seconds() < 0:
        alarm_today += datetime.timedelta(days=1)

    print(f"Alarm is set for {alarm_today}")

    # Calculate the time difference between now and the alarm time
    time_diff = (alarm_today - now).total_seconds()
    
    # Wait until the alarm time
    time.sleep(time_diff)

    # Perform the alarm action
    alarm_active = True
    display_message("Alarm! Check Pi 2")

def handle_client_connection(client_socket):
    global alarm_active
    while True:
        message = client_socket.recv(1024).decode()
        if message == "STOP":
            alarm_active = False
            display_message("Alarm Stopped")
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
        alarm_hour = int(input("Enter alarm hour (0-23): "))
        alarm_minute = int(input("Enter alarm minute (0-59): "))
        alarm_time = f"{alarm_hour:02}:{alarm_minute:02}"

        # Start the server in a separate thread
        server_thread = threading.Thread(target=start_server)
        server_thread.start()
        
        # Set the alarm
        set_alarm(alarm_time)
    except KeyboardInterrupt:
        pass
    finally:
        lcd.lcd_clear()

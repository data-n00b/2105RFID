import socket
import csv
from datetime import datetime, timedelta
import time
from RPLCD.i2c import CharLCD
import pandas as pd

# Function to read CSV file and return a list of tuples (time, message)
def read_csv_pd(file_path):
    '''
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        schedule = [(row[0], row[1], row[2]) for row in csv_reader]
    return schedule
    '''
    df_schedule = pd.read_csv(file_path,header=None)
    return df_schedule

# Function to send a message to the client
def send_message_to_client(message,piNumber):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    client_socket.connect((client_ip, client_port))
    client_socket.sendall(message.encode())
    client_socket.close()

# Function to start the server
def start_server(file_path):
    schedule = read_csv_pd(file_path)
#    for alarm_time, message, piNumber in schedule:
    for ind in schedule.index:
        alarm_time = schedule[0][ind]
        message = schedule[1][ind]
        piNumber = schedule[2][ind]
        # Wait until the specified time
        target_time = datetime.strptime(alarm_time, '%H:%M').time()
        now = datetime.now().time()
        wait_seconds = (datetime.combine(datetime.today(), target_time) - datetime.combine(datetime.today(), now)).total_seconds()
        if wait_seconds < 0:
            wait_seconds += 86400  # seconds in a day
        time.sleep(wait_seconds)

        # Print the message continuously and send it to the client
        print(f"Alarm: {message}")
        #Write To LCD display
        lcd.clear()
        lcd = CharLCD(i2c_expander = 'PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
        lcd.clear()
        lcd.write_string(message)
        send_message_to_client(message,piNumber)

        # Wait for confirmation from the client
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, server_port))
        server_socket.listen(1)
        conn, addr = server_socket.accept()
        confirmation = conn.recv(1024).decode()
        if confirmation == "CONFIRMED":
            print("Alarm confirmed by client. Stopping alarm.")
            conn.close()
            server_socket.close()
        else:
            print("Unexpected confirmation message")
            conn.close()
            server_socket.close()

if __name__ == "__main__":
    server_ip = "192.168.1.215"  # Server IP address
    server_port = 65432  # Server port
    client_ip = "192.168.1.204"    # Client IP address
    client_port = 65432  # Client port
    csv_file_path = "schedule.csv"
    start_server(csv_file_path)

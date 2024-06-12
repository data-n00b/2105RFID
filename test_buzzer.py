import socket
import csv
from datetime import datetime, timedelta
import time
from RPLCD.i2c import CharLCD
import pandas as pd



def send_message_to_client4(message):
    #client_ip = piNumber
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    client_socket.connect((client_ip4, client_port))
    client_socket.sendall(message.encode())
    client_socket.close()

# Function to start the server
def start_server():
    message = "This is a test message"
    lcd = CharLCD(i2c_expander = 'PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
    lcd.clear()
    #lcd = CharLCD(i2c_expander = 'PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
    lcd.clear()
    # Print the message continuously and send it to the client
    print(f"Alarm: {message}")
    #Write To LCD display
    
    #lcd = CharLCD(i2c_expander = 'PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
    lcd.clear()
    lcd.write_string(message)       
    send_message_to_client4(message)
        

if __name__ == "__main__":
    server_ip = "192.168.1.215"  # Server IP address
    server_port = 65432  # Server port
    client_ip4 = "192.168.1.241"
    client_port = 65432  # Client port      
    csv_file_path = "schedule.csv"
    start_server()

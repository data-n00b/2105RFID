import socket
import csv
from datetime import datetime, timedelta
import time
#from RPLCD.i2c import CharLCD
import pandas as pd
from Adafruit_IO import Client, Feed, Data
import calendar
import threading

calendar.setfirstweekday(calendar.SUNDAY)
clients = []
ip_dict = {1 : "192.168.1.204", 2 : "192.168.1.205", 3 : "192.168.1.206" }
# Function to read CSV file and return a list of tuples (time, message)
def read_csv_pd(file_path):
    df_schedule = pd.read_csv(file_path,header=None)
    return df_schedule

def handle_client(client_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if message == "CONFIRMED":
                print("Alarm confirmed by client. Stopping alarm.")
                #send_to_feed("E")
            else:
                print("Unexpected confirmation message")
                #send_to_feed("E")
            print(f"Received from {addr}: {message}")
            #broadcast_message(f"{addr}: {message}", client_socket)
        except ConnectionResetError:
            break
    client_socket.close()
    clients.remove(client_socket)

def broadcast_message(message, pi_number, sender_socket=None):
    for client in clients:
        
        if client != sender_socket and client.getsockname() == ip_dict[pi_number]:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def accept_connections(server):
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

'''
def send_to_feed(message):
    ADAFRUIT_IO_KEY = ''
    ADAFRUIT_IO_USERNAME = ''
    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    feed_name = 'cheekmate'
    feed = aio.feeds(feed_name)
    text_to_send = message
    data = Data(value=text_to_send)
    aio.create_data(feed.key, data)
'''
# Function to start the server
def start_server(file_path):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")

    accept_thread = threading.Thread(target=accept_connections, args=(server,))
    accept_thread.start()

    schedule = read_csv_pd(file_path)

    for ind in schedule.index:

        alarm_time = schedule[0][ind]
        message = schedule[1][ind]
        piNumber = schedule[2][ind]
        # Wait until the specified time
        target_time = datetime.strptime(alarm_time, '%H:%M').time()
        now = datetime.now().time()
        #To check the date (datetime.now().date().weekday())
        wait_seconds = (datetime.combine(datetime.today(), target_time) - datetime.combine(datetime.today(), now)).total_seconds()
        if wait_seconds < 0:
            wait_seconds += 86400  # seconds in a day
        time.sleep(wait_seconds)

        print(message)
        broadcast_message(message, piNumber)
        #send_to_feed(message)




if __name__ == "__main__":
    csv_file_path = "schedule.csv"
    start_server(csv_file_path)

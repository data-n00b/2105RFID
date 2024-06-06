import socket
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# Function to receive a message from the server
def receive_message_from_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((client_ip, client_port))
    server_socket.listen(1)
    conn, addr = server_socket.accept()
    message = conn.recv(1024).decode()
    conn.close()
    return message

# Function to read RFID card
def read_rfid():
    reader = SimpleMFRC522()
    try:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print(f"Card read with ID: {id}")
        return id
    finally:
        GPIO.cleanup()

# Function to send confirmation to the server
def send_confirmation_to_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_ip, server_port))
    server_socket.sendall("CONFIRMED".encode())
    server_socket.close()

if __name__ == "__main__":
    client_ip = "192.168.1.101"  # Client IP address
    client_port = 65432  # Client port
    server_ip = "192.168.1.100"  # Server IP address
    server_port = 65432  # Server port
    predefined_card_id = 123456789  # Example predefined card ID

    while True:
        message = receive_message_from_server()
        print(f"Received message: {message}")

        card_id = read_rfid()
        if card_id == predefined_card_id:
            send_confirmation_to_server()
            print("Confirmation sent to server.")
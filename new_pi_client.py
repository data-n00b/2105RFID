import socket
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(f"\nReceived: {message}")
                #GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
                #GPIO.setup(18, GPIO.OUT)  # Set pin as output
                #GPIO.output(18, GPIO.HIGH)
        except Exception as e:
            print("Connection closed by the server.")
            print(f"Connection error: {e}")
            client.close()
            break

       
def read_rfid():
    reader = SimpleMFRC522()
    try:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print(f"Card read with ID: {id}")
        return id
    finally:
        GPIO.cleanup()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '192.168.1.215'  # Replace with the server's IP address
    server_port = 9999
    predefined_card_id = 151042647098  

    try:
        client.connect((server_ip, server_port))
        print("Connected to server")

        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()

        while True:
            card_id = read_rfid()
            if card_id == predefined_card_id:
                message = "CONFIRMED"
                #GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
                #GPIO.setup(18, GPIO.OUT)  # Set pin as output
                #GPIO.output(18, GPIO.LOW)
                print("Confirmation sent to server.")
            if message.lower() == 'exit':
                break
            client.send(message.encode('utf-8'))
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()

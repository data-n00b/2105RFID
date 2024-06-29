import socket
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(f"\nReceived: {message}")
        except:
            print("Connection closed by the server.")
            client.close()
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '192.168.1.215'  # Replace with the server's IP address
    server_port = 9999

    try:
        client.connect((server_ip, server_port))
        print("Connected to server")

        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()

        while True:
            message = input("Enter message to send: ")
            if message.lower() == 'exit':
                break
            client.send(message.encode('utf-8'))
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()

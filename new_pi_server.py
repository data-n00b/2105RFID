import socket
import threading

clients = []

def handle_client(client_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received from {addr}: {message}")
            broadcast_message(f"{addr}: {message}", client_socket)
        except ConnectionResetError:
            break
    client_socket.close()
    clients.remove(client_socket)

def broadcast_message(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
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

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")

    accept_thread = threading.Thread(target=accept_connections, args=(server,))
    accept_thread.start()

    while True:
        server_message = input("Enter message to send to clients: ")
        broadcast_message(f"Server: {server_message}")

if __name__ == "__main__":
    main()

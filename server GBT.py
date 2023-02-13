import socket

def start_server(address, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen()
    print(f"Chat server started at {address}:{port}")

    clients = {}
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_socket.sendall(b"Enter your username: ")
        username = client_socket.recv(1024).decode().strip()
        if not username:
            username = str(client_address[0])
        clients[client_socket] = username
        print(f"Registered client '{username}'")
        client_socket.sendall(f"Welcome to the chat, {username}!".encode())
        broadcast_message(b"\n" + username.encode() + b" has joined the chat\n", client_socket)

        try:
            while True:
                message = client_socket.recv(1024)
                if not message:
                    break
                broadcast_message(username.encode() + b": " + message, client_socket)
        finally:
            client_socket.close()
            del clients[client_socket]
            broadcast_message(b"\n" + username.encode() + b" has left the chat\n")

def broadcast_message(message, sender_socket=None):
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.sendall(message)

if __name__ == "__main__":
    start_server("0.0.0.0", 8000)

import socket

def start_client(server_address, server_port, username=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    print(f"Connected to chat server at {server_address}:{server_port}")
    
    if not username:
        client_socket.sendall(b"")
        username = client_socket.recv(1024).decode().strip()
    else:
        client_socket.sendall(username.encode())
    print(f"Welcome to the chat, {username}!")

    try:
        while True:
            message = client_socket.recv(1024)
            print(message.decode(), end="")
            message = input().encode()
            client_socket.sendall(message)
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client("localhost", 8000)

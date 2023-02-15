from socket import *
import threading
import sys

def broadcast(message, sender=None):
    for client in clients:
        client.sendall(message)

def listUsers(message, connectionSocket):
    for value in clients.values():
        value = value + "\n"
        connectionSocket.send(value.encode())

def clientConnections(connectionSocket, addr):
    connectionSocket.send("Enter your username:".encode())
    username = connectionSocket.recv(1024).decode()
    clients[connectionSocket] = username
    print("Received connection from " + str(connectionSocket) + " with username " + username)
    connectionSocket.send(("Welcome to the chat " + username).encode())
    try:
         while True:
             message = connectionSocket.recv(1024).decode()
             if message.lower() == "/users":
                listUsers(message, connectionSocket)   
             else:    
                message = (username + ": " + message).encode()
                print(message.decode())
                broadcast(message, connectionSocket)

    except:
        connectionSocket.close()
        del clients[connectionSocket]
        broadcast((username + " has left the chat.").encode())

if len(sys.argv) != 3:
    print("usage: server.py port channels")
    exit()

serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print("The server is ready to receive")

clients = {}

while True:
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target=clientConnections, args=(connectionSocket, addr)).start()

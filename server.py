from socket import *
import threading
import sys

clients = {}
total = 0

def broadcast(message, sender=None):
    if(sender != None):
        client = clients[sender]
        client[1] += 1
    for client in clients:
        client.sendall(message)

def listUsers(connectionSocket):
    for value in clients.values():
        connectionSocket.send(value[0].encode())

def getStats(connectionSocket):
    client = clients[connectionSocket]
    connectionSocket.send((client[0] + " has sent " + str(client[1]) + " messages out of a total of " + str(total) + " messages.").encode())

def clientConnections(connectionSocket, addr):
    global total

    connectionSocket.send("Enter your username:".encode())
    username = connectionSocket.recv(1024).decode()
    clients[connectionSocket] = [username, 0]
    print("Received connection from " + str(connectionSocket) + " with username " + username)
    connectionSocket.send(("Welcome to the chat " + username).encode())
    try:
         while True:
            message = connectionSocket.recv(1024).decode()
            if message.lower() == "/users":
                listUsers(connectionSocket)
            elif message.lower() == "/stats":
                getStats(connectionSocket)
            else:
                total += 1
                print(total)
                message = (username + ": " + message).encode()
                print(message.decode())
                broadcast(message, connectionSocket)

    except ConnectionResetError:
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


while True:
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target=clientConnections, args=(connectionSocket, addr)).start()

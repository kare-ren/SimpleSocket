from socket import *
import threading
import sys

class channel:
    def __init__(self, name, clients, total):
        self.name = name
        self.clients = clients
        self.total = total
    #throw all functions into object object per channel
    def broadcast(self, message, sender=None):
        if(sender != None):
            client = self.clients[sender]
            client[1] += 1
        for client in self.clients:
            client.sendall(message)

    def listUsers(self, connectionSocket):
        for value in self.clients.values():
            connectionSocket.send(value[0].encode())

    def getStats(self, connectionSocket):
        client = self.clients[connectionSocket]
        connectionSocket.send((client[0] + "has sent " + str(client[1]) + " messages out of a total of " + str(self.total) + " messages.").encode())

    def clientConnections(self, connectionSocket, addr):
        self.total
        hostname= gethostname()   
        IPAddr= gethostbyname(hostname)   
        connectionSocket.send("Enter your username if no name type N:".encode())
        username = connectionSocket.recv(1024).decode()
        if username == 'n' or username == 'N':
            username = IPAddr
        self.clients[connectionSocket] = [username, 0] 
        print("Received connection from " + str(connectionSocket) + " with username " + username)
        connectionSocket.send(("Welcome to the chat room" + str(self.name) + ":" + username).encode())
        try:
            while True:
                message = connectionSocket.recv(1024).decode()
                if message.lower() == "/users":
                    self.listUsers(connectionSocket)
                elif message.lower() == "/stats":
                    self.getStats(connectionSocket)
                else:
                    self.total += 1
                    print(self.total)
                    message = (username + ": " + message).encode()
                    print(message.decode())
                    self.broadcast(message, connectionSocket)

        except ConnectionResetError:
            connectionSocket.close()
            del self.clients[connectionSocket]
            self.broadcast((username + " has left the chat.").encode())

if len(sys.argv) != 3:
    print("usage: server.py port channels")
    exit()
channelsList = []
for i in range (int((sys.argv[2]))):
    instance = channel(i, {}, 0) 
    channelsList.append(instance)
serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print("The server is ready to receive")


while True:
    connectionSocket, addr = serverSocket.accept()
    channelNum = int(connectionSocket.recv(1024).decode())
    spot = channelsList[channelNum] 
    threading.Thread(target=spot.clientConnections, args=(connectionSocket, addr)).start()

    

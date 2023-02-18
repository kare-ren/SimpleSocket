from socket import *
import threading
import sys
import os

# Channel class is responsible for running each chat channel
class Channel:
    def __init__(self, name, clients, total):
        self.name = name
        self.clients = clients
        self.total = total

    # Send message to all users in chat channel
    def broadcast(self, message, sender=None):
        if(sender != None):
            client = self.clients[sender]
            client[1] += 1
        for client in self.clients:
            client.sendall(message)

    # Send the user who asked a list of users in the chat channel
    def listUsers(self, connectionSocket):
        for value in self.clients.values():
            connectionSocket.send(value[0].encode())

    # Send the user who asked their statistics in the chat channel
    def getStats(self, connectionSocket):
        client = self.clients[connectionSocket]
        connectionSocket.send((client[0] + " has sent " + str(client[1]) + " messages out of a total of " + str(self.total) + " messages.").encode())

    # clientConnections runs the chat room. Get the username and then handle the send receive chat loop
    def clientConnections(self, connectionSocket, addr):
        hostname= gethostname()
        IPAddr= gethostbyname(hostname)
        connectionSocket.send("Enter your username if no name type N:".encode())
        username = connectionSocket.recv(1024).decode()
        if username.lower() == 'n':
            username = IPAddr
        self.clients[connectionSocket] = [username, 0] # clients[socket] = [username, messages_sent_by_user]
        print("Received connection from " + str(connectionSocket) + " with username " + username)
        connectionSocket.send(("Welcome to chat room " + str(self.name) + ": " + username).encode())
        self.broadcast((username + " has joined the chat.").encode())
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
        # if we get an error, the client has disconnected
        except ConnectionResetError:
            connectionSocket.close()
            del self.clients[connectionSocket]
            self.broadcast((username + " has left the chat.").encode())

# ALlow the server to send itself commands, return info from all of the chat channels
def getInput():
    while True:
        command = input()
        if command.lower() == "users":
            for channel in channelsList:
                for value in channel.clients.values():
                    print(value[0])
        elif command.lower() == "stats":
            atotal = 0
            for channel in channelsList:
                print(str(channel.name) + ":")
                for client in channel.clients.values():
                    print(client[0] + " has sent " + str(client[1]) + " messages")
                print("Total messages in channel: " + str(channel.total))
                atotal += channel.total
            print("Total messages in all channels: " + str(atotal))
        elif command.lower() == "quit":
            os._exit(1)

if len(sys.argv) != 3:
    print("usage: server.py port channels")
    exit()

# Initialize all of the channels based on command line input
channelsList = []
for i in range (int((sys.argv[2]))):
    instance = Channel(i, {}, 0)
    channelsList.append(instance)

# Initialize server based on command line input
serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print("The server is ready to receive")

# Start server command thread
threading.Thread(target=getInput, daemon=True).start()

# Start a new thread per client connected
while True:
    connectionSocket, addr = serverSocket.accept()
    channelNum = int(connectionSocket.recv(1024).decode())
    spot = channelsList[channelNum]
    threading.Thread(target=spot.clientConnections, args=(connectionSocket, addr), daemon=True).start()

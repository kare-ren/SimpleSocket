from socket import *
import threading
import queue
import sys

# Use queues for received output from the server and input from the client
inputBuf = queue.Queue()
outputBuf = queue.Queue()

def getInput():
    while True:
        inputBuf.put(input())

def getOutput():
    while True:
        outputBuf.put(clientSocket.recv(1024).decode())

if len(sys.argv) != 4:
    print("usage: client.py serverip port channel")
    exit()

# Get server info from command line
try:
    serverIP = int(sys.argv[1])
except(ValueError): # If we get an error, we're probably dealing with a string based ip (e.g. localhost). If not, it's bad input and shouldn't work.
    serverIP = sys.argv[1]

serverPort = int(sys.argv[2])
serverChannel = (sys.argv[3])

# Connect to the server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP,serverPort))
clientSocket.send(serverChannel.encode())

# Get username
print(clientSocket.recv(1024).decode())
username = input()
clientSocket.send(username.encode())
print(clientSocket.recv(1024).decode())
print("Type 'quit' to close the client.")
# Start input/output receiving threads
threading.Thread(target=getInput, daemon=True).start()
threading.Thread(target=getOutput, daemon=True).start()

# When the input/output buffers aren't empty, empty them and deal with it
while True:
    while(inputBuf.empty() == False):
        message = inputBuf.get()
        if(message == "quit"):
            clientSocket.close()
            exit()
        clientSocket.send(message.encode())

    while(outputBuf.empty() == False):
        print(outputBuf.get())

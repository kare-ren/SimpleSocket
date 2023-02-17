from socket import *
import threading
import queue
import sys


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

serverName = "localhost"
serverIP = int(sys.argv[1])
serverPort = int(sys.argv[2])
serverChannel = (sys.argv[3])
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
clientSocket.send(serverChannel.encode())
print(clientSocket.recv(1024).decode())
username = input()
clientSocket.send(username.encode())
print(clientSocket.recv(1024).decode())

threading.Thread(target=getInput, daemon=True).start()
threading.Thread(target=getOutput, daemon=True).start()

while True:
    while(inputBuf.empty() == False):
        message = inputBuf.get()
        if(message == "quit"):
            exit()
        clientSocket.send(message.encode())

    while(outputBuf.empty() == False):
        print(outputBuf.get())


clientSocket.close()

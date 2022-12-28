from socket import *
import sys

proxyName = '127.0.0.1'
proxyPort = 1234

message = "Hey I am the first client !"

for i in range (10):
	clientSocket = socket(AF_INET,SOCK_STREAM)
	clientSocket.connect((proxyName, proxyPort))
	clientSocket.sendall(message.encode('utf-8')) #envoie du msg au  proxy
	response = clientSocket.recv(2048) #reponse du proxy
	print(' server answer is :', response.decode('utf-8')) #affichage de l>
	#clientSocket.close()
clientSocket.close()


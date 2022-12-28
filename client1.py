from socket import *
import sys
from threading import *

proxyName = '127.0.0.1'
proxyPort = 1234

#clientSocket = socket(AF_INET,SOCK_STREAM) #creation socket client
#clientSocket.connect((proxyName, proxyPort)) #connecion au proxy
#message = input('message à envoyer au serveur').encode('utf-8') #le client tape>
message = "This is...the second client !"

for i in range (10):
	clientSocket = socket(AF_INET,SOCK_STREAM)
	clientSocket.connect((proxyName, proxyPort))
	clientSocket.sendall(message.encode('utf-8')) #envoie du msg au  proxy
	response = clientSocket.recv(2048) #reponse du proxy
	print(' server answer is :', response.decode('utf-8')) #affichage de l>
	#clientSocket.close()


from socket import *
import threading as t
import sys

serverName = '127.0.0.1'
serverPort = 5678
proxyPort = 1234

def handle_client(connectionClient):
	request_client = connectionClient.recv(2048) # reception de la requête du client
	print ('the message received by the client is :', request_client)
	connectionServer = socket(AF_INET, SOCK_STREAM) #socket pour se connecter au serveur
	connectionServer.setsockopt (SOL_SOCKET,SO_REUSEADDR,1)
	connectionServer.connect ((serverName, serverPort)) #connection à la socket server sur le port 5678
	connectionServer.sendall(request_client) # envoie de la requête au serveur
	print (' I send the message to the server')
	response = connectionServer.recv(2048) #reponse du serveur
	connectionClient.sendall ( response) # envoie du msg au client
	print ( ' I send the response to the client')
	connectionClient.close()
	#connectionServer.close()


def main():
	proxySocket = socket(AF_INET, SOCK_STREAM) #socket du proxy
	proxySocket.setsockopt (SOL_SOCKET,SO_REUSEADDR,1)
	proxySocket.bind(((''),proxyPort)) # ecoute sur le port du proxy 1234
	proxySocket.listen(15)
	print ( 'proxy ready ')
	while True:
		connectionClient, _  = proxySocket.accept() # socket qui accepte les requetes des clients
		t.Thread(target=handle_client(connectionClient,)).start()
		print ( 'thread launched' )
main()

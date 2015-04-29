import socket
import os

global inIP
inIP = "127.0.0.1"

global inPORT
inPORT = 2020

global outIP
outIP = "127.0.0.1"

global outPORT
outPORT = 9090

global mirrorIP
mirrorIP = "127.0.0.1"

global mirrorPORT
mirrorPORT = 9090

inSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
inSocket.bind((inIP, inPORT))
inSocket.listen(5)

while True:
	
	clientSocket, address = inSocket.accept()
	
	pid = os.fork()
	
	if(pid == 0):
		try:
			inSocket.close()
			data = ""
			
			while True:
				string = clientSocket.recv(1024)
				if not string:
					break
				data = data + string
			
			print "\n\n\t\t\t-------------------------\n-> ", address, "---: \n", data
			
			outSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			outSocket.connect((outIP, outPORT))

			mirrorSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			mirrorSocket.connect((mirrorIP, mirrorPORT))
			
			outSocket.send(data)
			mirrorSocket.send(data)
			
		except Exception as e:
			print e
			print("Error!")
			
		finally:
			clientSocket.close()
			os._exit(0)
	else:
		clientSocket.close()


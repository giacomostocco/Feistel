from bitarray import bitarray
import time
import socket
import multiprocessing
from Function import Function
import Util

start = time.time()

bytes = bitarray()
data = bitarray()
output = bitarray()

with open (Util.inputFile, "rb") as f:
	bytes.fromfile(f)

print "Data length:", ((bytes.length()/8)/1024), "KB"
for i in range(bytes.length()%32):
	bytes.extend("0")

for i in range(bytes.length()/32):
	data = bytes[(0+(32*i)):(32+(32*i))]
	if data.length() != 32:
		print data.length()
		
	temp = bitarray(data)
	for j in range(Util.ITERATIONS):
		inLi = temp[0:16]
		inRi = temp[16:]
		temp = bitarray()		
		temp.extend(inRi)	
		temp.extend(inLi ^ (Function.permutation(inRi, Util.KEY)))
	output.extend(temp)

fOut = open(Util.encodedFile, "wb")
output.tofile(fOut)
fOut.close()

print "Encoded succesfully: elapsed time", time.time()-start, "seconds."

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((Util.ADDRESS, Util.ENCODEPORT))

file = open(Util.encodedFile, "rb")

print "Sending to server ..."

while True: 
	data = file.read(Util.SIZE)
	socket.send(data)	
	if data == "": 
	    	break	   
file.close()
socket.close()

print "Terminated."

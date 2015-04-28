from bitarray import bitarray
import time
from Function import Function
from Server import ServerUDP
import Util

socket = ServerUDP.initServerSocket(Util.ADDRESS, Util.DECODEPORT)
print "Running and waiting..."

try:
	file = open(Util.encodedFile, "wb")		
	
	data = ServerUDP.readSocket(socket)
	print "Receiving data ..."
	
	file.write(data)	
	file.close()
	
	print "Starting the decoding process ..."

	start = time.time()
	
	bytes = bitarray()
	data = bitarray()
	output = bitarray()
	
	with open (Util.encodedFile, "rb") as f:
		bytes.fromfile(f)
	
	print "Data length:", ((bytes.length()/8)/1024), "KB"
	
	for i in range(bytes.length()/32):
		data = bytes[(0+(32*i)):(32+(32*i))]
		temp = bitarray(data)
		for j in range(Util.ITERATIONS):
			inLi = temp[0:16]
			inRi = temp[16:]
			temp = bitarray()		
			temp.extend(inRi ^ (Function.permutation(inLi, Util.KEY)))
			temp.extend(inLi)	
		output.extend(temp)
	
	while output[output.length()-1] == 0:
	    output.pop(output.length()-1)
	output.fill()
	
	fOut = open(Util.decodedFile, "wb")
	output.tofile(fOut)
	fOut.close()
	
	print "Decoded succesfully: elapsed time", time.time()-start, "seconds."	
	
except Exception as e:
	print e
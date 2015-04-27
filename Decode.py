from bitarray import bitarray
import time
from Function import Function

global ITERATIONS
ITERATIONS = 16

global KEY
KEY = 9

global encodedFile
encodedFile = "encoded.pgm"

global decodedFile
decodedFile = "decoded.pgm"

start = time.time()

bytes = bitarray()
data = bitarray()
output = bitarray()

with open (encodedFile, "rb") as f:
	bytes.fromfile(f)

print bytes.length()

for i in range(bytes.length()/32):
	data = bytes[(0+(32*i)):(32+(32*i))]
	temp = bitarray(data)
	for j in range(ITERATIONS):
		inLi = temp[0:16]
		inRi = temp[16:]
		temp = bitarray()		
		temp.extend(inRi ^ (Function.permutation(inLi, KEY)))
		temp.extend(inLi)	
	output.extend(temp)

while output[output.length()-1] == 0:
    output.pop(output.length()-1)
output.fill()

fOut = open(decodedFile, "wb")
output.tofile(fOut)
fOut.close()

print "Decoded succesfully: elapsed time", time.time()-start, "seconds."

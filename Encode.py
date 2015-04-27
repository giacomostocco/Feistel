from bitarray import bitarray
import time
import multiprocessing
from Function import Function

global ITERATIONS
ITERATIONS = 5

global KEY
KEY = 9

global inputFile
inputFile = "Scrivania/test.CR2"

global encodedFile
encodedFile = "Scrivania/encoded.CR2"

def feistel(data):
	temp = bitarray(data)
	for j in range(ITERATIONS):
		inLi = temp[0:16]
		inRi = temp[16:]
		temp = bitarray()		
		temp.extend(inRi)	
		temp.extend(inLi ^ (Function.permutation(inRi, KEY)))
	return temp

start = time.time()

bytes = bitarray()
data = bitarray()
output = bitarray()

with open (inputFile, "rb") as f:
	bytes.fromfile(f)

print bytes.length()

arguments = []
for i in range(bytes.length()/32):
	arguments.append(bytes[(0+(32*i)):(32+(32*i))])

pool = multiprocessing.Pool(processes = 8)
encodedBlocks = pool.map(feistel, arguments)

for i in encodedBlocks:
	output.extend(i)

#for i in range(bytes.length()/32):
#	data = bytes[(0+(32*i)):(32+(32*i))]
#	temp = bitarray(data)
#	for j in range(ITERATIONS):
#		inLi = temp[0:16]
#		inRi = temp[16:]
#		temp = bitarray()		
#		temp.extend(inRi)	
#		temp.extend(inLi ^ (Function.permutation(inRi, KEY)))
#	output.extend(temp)

fOut = open(encodedFile, "wb")
output.tofile(fOut)
fOut.close()

print "Encoded succesfully: elapsed time", time.time()-start, "seconds."

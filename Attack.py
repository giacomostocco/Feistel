from bitarray import bitarray
import time
import random
import hashlib
from Function import Function

global ITERATIONS
ITERATIONS = 16

global encodedFile
encodedFile = "encoded.pgm"

global sampleFile
sampleFile = "decoded.pgm"

global decodedFile
decodedFile = "attack_decoded.pgm"

start = time.time()

bytes = bitarray()
data = bitarray()
output = bitarray()

with open (encodedFile, "rb") as f:
    bytes.fromfile(f)

print bytes.length()

keys = {}
key = random.randint(1,31)
keys[key] = True
found = False
while not found:
    for i in range(bytes.length()/32):
        data = bytes[(0+(32*i)):(32+(32*i))]
        temp = bitarray(data)
        for j in range(ITERATIONS):
            inLi = temp[0:16]
            inRi = temp[16:]
            temp = bitarray()        
            temp.extend(inRi ^ (Function.permutation(inLi, key)))
            temp.extend(inLi)    
        output.extend(temp)
    
    fOut = open(decodedFile, "wb")
    output.tofile(fOut)
    fOut.close()
    
    with open(sampleFile, "rb") as fSample:
        sampleContent = fSample.read()
        
    md5sample = hashlib.md5()
    md5sample.update(sampleContent)
    
    with open(decodedFile, "rb") as fDecoded:
        decodedContent = fDecoded.read()
        
    md5decoded = hashlib.md5()
    md5decoded.update(decodedContent)
    
    if md5decoded == md5sample:
        found = True
    else:
        while key in keys:
            key = random.randint(1,31)
        keys[key] = True

print "Decoded succesfully: elapsed time", time.time()-start, "seconds, key", key,"."
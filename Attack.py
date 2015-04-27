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
sampleFile = "lenna.pgm"

global decodedFile
decodedFile = "attack_decoded.pgm"

start = time.time()

bytes = bitarray()

with open (encodedFile, "rb") as f:
    bytes.fromfile(f)

print bytes.length()

with open(sampleFile, "rb") as fSample:
    sampleContent = fSample.read()        
md5sample = hashlib.md5()
md5sample.update(sampleContent)
    
keys = {}
key = random.randint(1,31)
keys[key] = True
found = False
while not found:
    print "Decoding with key", key, "..."
    output = bitarray()
    data = bitarray()
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
        
    while output[output.length()-1] == 0:
        output.pop(output.length()-1)
    output.fill()
    
    fOut = open(decodedFile, "wb")
    output.tofile(fOut)
    fOut.close()
    
    with open(decodedFile, "rb") as fDecoded:
        decodedContent = fDecoded.read()
        
    md5decoded = hashlib.md5()
    md5decoded.update(decodedContent)
    print md5decoded.hexdigest()
    print md5sample.hexdigest()
    if md5decoded.hexdigest() == md5sample.hexdigest():
        found = True
    else:
        while key in keys:
            key = random.randint(1,31)
        keys[key] = True

print "Decoded succesfully: elapsed time", time.time()-start, "seconds, key", key,"."
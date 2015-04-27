from bitarray import bitarray
import time
import random
import hashlib
from Function import Function
from Server import ServerUDP
import Util

socket = ServerUDP.initServerSocket(Util.ADDRESS, Util.ATTACKPORT)
print "Running and waiting..."

try:
    file = open(Util.encodedAttackFile, "wb")        
    
    data = ServerUDP.readSocket(socket)
    print "Receiving data ..."
    
    file.write(data)    
    file.close()
    
    print "Starting the attack operations ..."

    start = time.time()
    
    bytes = bitarray()
    
    with open (Util.encodedAttackFile, "rb") as f:
        bytes.fromfile(f)
    
    print "Data length:", ((bytes.length()/8)/1024), "KB"
    
    with open(Util.sampleAttackFile, "rb") as fSample:
        sampleContent = fSample.read()        
    md5sample = hashlib.md5()
    md5sample.update(sampleContent)
        
    keys = {}
    key = random.randint(1,31)
    keys[key] = True
    found = False
    while not found:
        print "\nDecoding with key", key, "..."
        output = bitarray()
        data = bitarray()
        for i in range(bytes.length()/32):
            data = bytes[(0+(32*i)):(32+(32*i))]
            temp = bitarray(data)
            for j in range(Util.ITERATIONS):
                inLi = temp[0:16]
                inRi = temp[16:]
                temp = bitarray()        
                temp.extend(inRi ^ (Function.permutation(inLi, key)))
                temp.extend(inLi)    
            output.extend(temp)
            
        while output[output.length()-1] == 0:
            output.pop(output.length()-1)
        output.fill()
        
        fOut = open(Util.decodedAttackFile, "wb")
        output.tofile(fOut)
        fOut.close()
        
        with open(Util.decodedAttackFile, "rb") as fDecoded:
            decodedContent = fDecoded.read()
            
        md5decoded = hashlib.md5()
        md5decoded.update(decodedContent)
        print "Decoded file MD5:", md5decoded.hexdigest()
        print "Sample file MD5: ", md5sample.hexdigest()
        if md5decoded.hexdigest() == md5sample.hexdigest():
            found = True
        else:
            while key in keys:
                key = random.randint(1,31)
            keys[key] = True
    
    print "\nDecoded succesfully: elapsed time", time.time()-start, "seconds, key", key,"."
    
except Exception as e:
    print e
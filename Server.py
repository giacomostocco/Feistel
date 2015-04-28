import socket
import Util

class Server:   
    
    @staticmethod
    def initServerSocket(address, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((address, port))
        s.listen(5)
        return s
    
    @staticmethod
    def readSocket(socket):
        text = ""
        
        while True:
            string, address = socket.recv(Util.SIZE)
            if string == "":
                break
            text = text + string
        return text

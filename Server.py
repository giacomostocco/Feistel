import socket

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
        data = ""
        
        while True:
            tempData = socket.recv(1024)
            if tempData == "":
                break
            data = data + tempData
        return data

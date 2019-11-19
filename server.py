###############################
#This class serves to send messages from the server to the various ports via UDP sockets 
class Server:
    def __init__(self, port=1234, encoding='utf-8'):
        self.__port__ = port
        self.__connections__ = list()
        self.__encoding__ = encoding
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', port))

    def recieveFromLAD(self):
        buf, address = self.socket.recvfrom(self.__port__)
        addr, port = address
        return buf.decode(self.__encoding__), addr, port
    
    def recieveFromAndroid(self):
        buf, address = self.socket.recvfrom(self.__port__)
        addr, port = address
        return buf.decode(self.__encoding__), addr, port
        #todo: update database
    
    #we're hard coding which port each device is listening to and sending from 
    def sendToLAD(self, msg, address, port):
        data = msg.encode("utf-8")
        self.socket.sendto(data, (address, port))
        print("Sending to address {}".format(address))
        print("Sending: {}".format(msg)) 

    def sendToAndroid(self, msg, address, port):
        data = msg.encode("utf-8")
        self.socket.sendto(data, (address, port))
        print("Sending to address {}".format(address))
        print("Sending: {}".format(msg)) 
    
    def close(self):
        self.socket.shutdown(1)
        print("Connection Closed")

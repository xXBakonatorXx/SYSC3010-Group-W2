#!/bin/bash

import socket
import sys
import time


class Server:
    def __init__(self, port=8888, encoding='utf-8'):
        self.__port__        = port
        self.__connections__ = list()
        self.__encoding__    = encoding
        self.socket          = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.socket.bind(('', port))
        print("Server is listening on port {}".format(port))

    def receive(self):
        """ (None) -> str, str, int

        receives data sent to server and returns message, and the ip and port of sender

        >>> server.receive()
        ("hello, world", "127.0.0.1", 1001)
        """
        buf, address     = self.socket.recvfrom(self.__port__)
        print("Received data from {}".format(address))
        print("Recieved: {}".format(buf))
        addr, port = address
        return buf.decode(self.__encoding__), addr, port

    def send(self, msg, address, port):
        """ (str, str, int) -> None

        sends messsge to specified ip on a port

        >>> server.send("hello, world", "127.0.0.1", 1001)
        """
        data = msg.encode("utf-8")
        self.socket.sendto(data, (address, port))
        print("Sending to address {}".format(address))
        print("Sending: {}".format(msg))        

    def close(self):
        """ (None) -> None

        Closes connection
        """
        self.socket.shutdown(1)
        print("Connection closed")

class Client:
    def __init__(self, address='127.0.0.1', port=8888, encoding='utf-8'):
        self.__address__  = address
        self.__port__     = port
        self.__encoding__ = encoding 
        self.socket       = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       
        print("Client ready to send data to {} on port {}".format(address, port))

    def receive(self):
        """ (None) -> str

        receives data sent to client from the server and returns message

        >>> client.receive()
        "hello, world"
        """
        buf, address     = self.socket.recvfrom(self.__port__)
        print("Received data from {}".format(address))
        print("Recieved: {}".format(buf))
        return buf.decode(self.__encoding__)

    def send(self, msg):
        """ (str) -> None

        sends messsge to server

        >>> client.send("hello, world", "127.0.0.1", 1001)
        """
        data = msg.encode("utf-8")
        self.socket.sendto(data, (self.__address__, self.__port__))
        print("Sending to address {}".format(self.__address__))
        print("Sending: {}".format(msg))

    def getAddress(self):
        """ (None) -> str

        gets ip of the server
        
        >>> client.getAddress()
        "127.0.0.1"
        """
        return self.__address__

    def getPort(self):
        """ (None) -> int

        gets port used to connect to the server
        
        >>> client.getPort()
        1001
        """
        return self.__port__

    def close(self):
        """ (None) -> None

        Closes connection
        """
        self.socket.shutdown(1)
        print("Connection closed")

def __testServer__(address, port):
    s = Server(port)
    s.send("","localhost",8888)
    s.close()

def __testClient__(address, port):
    c = Client(address, port)
    c.send("")
    c.close()

def __testAll__(address, port):
    s, c = Server(port), Client(address, port)
    c.send("Message")
    data, addr, port = s.receive()
    s.send("ACK: "+data.decode('utf-8'), addr, port)
    c.receive()
    c.close()
    s.close()

if __name__ == "__main__":
    address, port = "127.0.0.1", 1001
    #__testServer__(port)
    #__testClient__(address, port)
    __testAll__(address, port)
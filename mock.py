#This file will serve as a mock object for database testing

#Mock LAD RPi - port 520
# IP - localhost (for testing purposes)

#Mock Android - Port 510
# IP - localhost (for testing purposes)

#Requirements: 
    #Send Messages
    #recieve messages 
import socket 
import sys
import select

HOST = '127.0.0.1'

def recieveData(port):
    recPort = port
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, recPort))
        print("waiting for message")
        while True:
            data, addr = s.recvfrom(1024)
            recieved = str(data)
            print("recieved message:", recieved)
            try:
                while(data):
                    #do nothing 
            except timeout:
                print("file downloaded")       

def fileTransfer(fileName):
    s =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 520
    buffer = 1024
    addr = (HOST, port)

    file_name = fileName

    f = open(file_name, 'r')
    data = f.read(buffer)
    bytestream = bytearray()
    bytestream.extend(map(ord, data))
    while(data):
        if(s.sendto(bytestream, addr)):
            print("sending...")
            data = f.read(buffer)
    print(bytestream)
    s.close()
    f.close()

if __name__ == '__main__':
    fileTransfer('test3.json')
    





    




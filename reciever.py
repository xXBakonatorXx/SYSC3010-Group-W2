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

if __name__ == '__main__':
    recieveData(520)
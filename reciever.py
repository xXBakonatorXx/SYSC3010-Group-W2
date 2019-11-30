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
                while(recieved):
                    print("working")#do nothing
            except:
                print("timeout, please try again")
            finally:
                s.close()
                print("connection closed")
if __name__ == '__main__':
    recieveData(510)
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

    
import socket, sys, time

host = sys.argv[1]
textport = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)

while 1:
    print ("Enter data to transmit: ENTER to quit")
    data = sys.stdin.readline().strip()
    if not len(data):
        break
#    s.sendall(data.encode('utf-8'))
    s.sendto(data.encode('utf-8'), server_address)

s.shutdown(1)


    





    




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
import time
from LADfunctions import sql_to_json, json_to_dict
import json
import sqlite3

HOST = '127.0.0.1'


host = sys.argv[1]
textport = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)


print("data transmitting...")
data = sql_to_json('items')
print(type(data))
datastring = ""
for var in data:
    datastring += str(data) + ", "    
bytearr = bytearray(datastring, "utf-8")
#    s.sendall(data.encode('utf-8'))
s.sendto(bytearr, server_address)

s.shutdown(1)


    





    




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

#Assumptions made based on lack of support -
#messages will be sent in the format of {command: "", table: "", {args}}
#command is a key, and table is a value of command, and also a key for nested dict of args
#example: {"delete": "items": {"name": "plate", "location": "kitchen"}}

HOST = '127.0.0.1'  


host = sys.argv[1]
textport = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)


print("data transmitting...")
data = json_to_dict("decode.json")
datastring = str(data)  
bytearr = bytearray(datastring, "utf-8")
s.sendto(bytearr, server_address)

s.shutdown(1)


    





    




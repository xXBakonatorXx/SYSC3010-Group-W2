import socket 
import sys
import select
import json
from LADfunctions import json_to_dict, sql_to_json, insert_row, delete_row
import re

HOST = '127.0.0.1'

def recieveData(port):
    recPort = port
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, recPort))
        print("waiting for message")
        data, addr = s.recvfrom(1024)
        print("recieved message:", data)
            #decode logic here
        recieved = str(data)
        recieved = recieved.replace('"', '')
        recieved = recieved.replace("'", '')
        dataDict = re.split("{|}|: |, |\n|\t|' '", recieved)
        print(dataDict)
        del dataDict[0]
        del dataDict[1]
        del dataDict[2]
        i = 3
        while i >= 1:
            del dataDict[-i]
            i -= 1
        for num in dataDict:
            if num == "":
                del num
            elif num == "b":
                del num
        print(dataDict)    
        if dataDict[0] == 'delete': #THIS WORKS 
            print("command recieved: delete")
            delete_row(dataDict[1], dataDict[3])
        elif dataDict[0] == 'insert':
            print("command recieved: insert")
            insert_row(newList = list(chain(dataDict[1:])))
        #the rest of the logic goes here
        #print("timeout, please try again")
        print("connection closed")
        s.close()
            
if __name__ == '__main__':
    recieveData(510)
import socket 
import sys
import select
from LADfunctions import json_to_dict, sql_to_json, insert_row, delete_row
import ast

HOST = '127.0.0.1'

def recieveData(port):
    recPort = port
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, recPort))
        print("waiting for message")
        try:
            data, addr = s.recvfrom(1024)
            recieved = str(data)
            print("recieved message:", recieved)
            #decode logic here
            dataDict = ast.literal_eval(recieved)
            print(dataDict)
            if dataDict.keys() == 'delete':
                print("command recieved: delete")
            
        except:
            print("timeout, please try again")
        finally:
            print("connection closed")
            s.shutdown(1)
            s.close()
            
if __name__ == '__main__':
    recieveData(510)
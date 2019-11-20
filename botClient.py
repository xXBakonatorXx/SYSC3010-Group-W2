from UDPSocket import Client
import os, time
from LADfunctions import LADfunctions
# Identifying Prefix
PREFIX   = "bot"

# Database file
CACHE    = "cache.txt"
ENCODING = "utf-8"

# Codes for sending and receiving
UPDATE   = "update"
CONTINUE = "continue"
EOF      = "***" 

def encode_data(key, data):

    encoded = str(key)
    for d in data:
        encoded += "\t" + d
    encoded += "\n"

    return encoded

def send(cache, client):
    data = cache.getData()
    for key in data.keys():
        encoded = encode_data(key, data)
        client.send(PREFIX+encoded)
    client.send(PREFIX+EOF)

def check_database(cache, client):
    client.send(PREFIX+UPDATE)
    update = client.receive()
    if update == UPDATE:
        data = None
        while (True):
            data = client.receive()
            if data == EOF:
                break
            
            data = data.split()
            idx = data.pop(0)
            
            cache.add(idx, data)
        cache.write()
        return True
    else:
        return False

if __name__ == "__main__":
    client = Client("127.0.0.1",510)
    cache  = Cache(CACHE)
    while (True):
        check_database(cache, client) 
        cache.print()  
        time.sleep(10)     

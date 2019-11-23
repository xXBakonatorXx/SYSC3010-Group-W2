# Source: https://pymotw.com/2/socket/udp.html

import socket, sys, time
import json

host = sys.argv[1]
textport = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)

json_dict = json.loads('{ "name":"John", "age":30, "city":"New York"}')

for msg in range(10):
    data = json.dumps(json_dict)

    s.sendto(str(data).encode('utf-8'), server_address)
    sentBack = None
    while True:
        buf, addess = s.recvfrom(1001)
        print("Recieved: {}".format(buf))
        if buf:
            break

s.close()


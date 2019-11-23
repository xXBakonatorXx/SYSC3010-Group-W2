# Source: https://pymotw.com/2/socket/udp.html

import socket, sys, time
import random

host = sys.argv[1]
textport = sys.argv[2]
n = sys.argv[3]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)

for msg in range(int(n)):
    data = random.randint(1,101)

    s.sendto(str(data).encode('utf-8'), server_address)
    sentBack = None
    while True:
        buf, addess = s.recvfrom(1001)
        print("Recieved: {}".format(buf))
        if buf:
            break

s.close()


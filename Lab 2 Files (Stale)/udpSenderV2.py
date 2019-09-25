# Source: https://pymotw.com/2/socket/udp.html

import socket, sys, time

host = sys.argv[1]
textport = sys.argv[2]
nMessages = sys.argv[3]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)

for msg in range(int(nMessages)):
    data = "Message{}".format(msg+1)
    if not len(data):
        break
    s.sendto(data.encode('utf-8'), server_address)
    sentBack = None
    while True:
        buf, addess = s.recvfrom(1001)
        print("Recieved: {}".format(buf))
        if buf:
            break

s.close()


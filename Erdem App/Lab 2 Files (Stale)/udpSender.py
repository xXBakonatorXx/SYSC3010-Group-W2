<<<<<<< HEAD
# Source: https://pymotw.com/2/socket/udp.html

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

=======
# Source: https://pymotw.com/2/socket/udp.html

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

>>>>>>> 32098838254426a7f77a10c6e2f7f7ac09f194ee

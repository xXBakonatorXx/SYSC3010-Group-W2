# Source: https://pymotw.com/2/socket/udp.html

import socket, sys, time

host = sys.argv[1]
textport = sys.argv[2]
n = int(sys.argv[3])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)
currentN = 1;
while currentN <= n:
	data = "Message{}".format(currentN)
	currentN += 1
	print("Msg SENT: " + data) #for debugging
	if not len(data):
		break
	s.sendto(data.encode('utf-8'), server_address)
	while True:
		buf, address = s.recvfrom(port)
		print("ACK: {}".format(buf))
		if buf:
			break

s.shutdown(1)
s.close()

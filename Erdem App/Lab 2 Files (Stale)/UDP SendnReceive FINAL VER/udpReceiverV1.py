# Source: https://pymotw.com/2/socket/udp.html

import socket, sys, time

textport = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
# server_address = ('localhost', port) Originally
server_address = ('', port)
s.bind(server_address)

while True:

	print ("Waiting to receive on port %d : press Ctrl-C or Ctrl-Break to stop " % port)
	buf, address = s.recvfrom(port)
	s.sendto("ACK:{}".format(buf).encode("utf-8") ,address)
	if not len(buf):
		break
	print ("Received %s bytes from %s %s: " % (len(buf), address, buf ))

s.shutdown(1)
s.close()
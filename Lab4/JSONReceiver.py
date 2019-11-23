# Source: https://pymotw.com/2/socket/udp.html

import socket, sys, time, json

textport = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = ('', port)
s.bind(server_address)

while True:

    print ("Waiting to receive on port %d : press Ctrl-C or Ctrl-Break to stop " % port)

    buf, address = s.recvfrom(port)
    data = "ACK: {}".format(buf)
    s.sendto(data.encode("utf-8") ,address)
    if not len(buf):
        break
    print ("Received %s bytes from %s %s: " % (len(buf), address, buf ))
    
    json_dict = json.loads(buf.decode('utf-8'))
    
    for key in json_dict.keys():
        print("{} : {}".format(key, json_dict[key]))
              
s.shutdown(1)

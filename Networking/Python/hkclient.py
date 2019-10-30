import UDPSocket

if __name__ == "__main__":
    host, port = "127.0.0.1", 8888
    
    client = UDPSocket.Client(host, port)
    while(True):
        msg = input("{}:{}$ ".format(host, port))
        client.send(msg)
        data = client.receive()
        print(data)
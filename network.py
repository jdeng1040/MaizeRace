import json
import socket
import helper

class Client:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "35.3.210.91"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.name = name
    
    def sendConnect(self):
        """
        Tell the server we are connecting
        """
        self.client.connect(self.addr)
        data = helper.toJSON({
            "type": "ENTER",
            "name": self.name
        })
        print("sending: ", data)
        self.client.sendall(data)

        recv_data = json.loads(self.client.recv(helper.PACKET_SIZE).decode())
        print("Received: ", recv_data)
        return recv_data
            
    
    def sendPosition(self, currentPosition):
        """
        Send our current position and receive response (everyone's position or game ended)
        """
        pass


c = Client("jason")
c.sendConnect()



class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "35.3.210.91"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
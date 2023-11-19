import json
import socket
import helper

class Client:
    def __init__(self, name, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 5555
        self.addr = (self.server, self.port)
        self.client.connect(self.addr)
        self.name = name
    
    def sendConnect(self):
        """
        Tell the server we are connecting
        """
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

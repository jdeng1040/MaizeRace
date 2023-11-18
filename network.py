import json
import socket
import sys
import helper
import maze


class Client:
    def __init__(self, ip, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 5555
        self.addr = (self.server, self.port)
        self.name = name

    def sendConnect(self):
        """
        Tell the server we are connecting
        """
        self.client.connect(self.addr)
        data = helper.toJSON({
            "type": helper.ENTER,
            "name": self.name
        })
        print("sending: ", data)
        self.client.sendall(data)

        recv_data = json.loads(self.client.recv(helper.PACKET_SIZE).decode())
        print("Received: ", recv_data)

        if recv_data["type"] == "PLAYERS":
            # do nothing
            pass
        elif recv_data["type"] == "BEGIN":
            recv_data["maze"] = maze.deserialize_maze(recv_data["maze"])
        else:
            print("unknown type")
            sys.exit(1)

        return recv_data

    def sendPosition(self, currentPosition):
        """
        Send our current position and receive response (everyone's position or game ended)
        """
        pass


if len(sys.argv) != 3:
    print("need ip + client name", sys.argv)
    sys.exit(1)

c = Client(sys.argv[1], sys.argv[2])
c.sendConnect()

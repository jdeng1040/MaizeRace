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
        self.client.connect(self.addr)

    def sendConnect(self):
        """
        Tell the server we are connecting
        """
        data = helper.toJSON({
            "type": helper.ENTER,
            "name": self.name
        })
        print("sending: ", data)
        self.client.sendall(data)

        recv_data = json.loads(self.client.recv(helper.PACKET_SIZE, socket.MSG_WAITALL).decode())
        print("Received: ", recv_data)

        if recv_data["type"] == "PLAYERS":
            # do nothing
            return recv_data
        elif recv_data["type"] == "BEGIN":
            recv_data["maze"] = maze.deserialize_maze(recv_data["maze"])
            maze.print_maze(recv_data["maze"], [])
        else:
            print("unknown type")
            sys.exit(1)

        return recv_data

    def sendPosition(self, currentPosition, name):
        """
        Send our current position and receive response (everyone's position or game ended)
        """
        data = helper.toJSON({
            "type": helper.POSITION,
            "position": currentPosition,
            "name": name,
        })

        self.client.sendall(data)

        recv_data = json.loads(self.client.recv(helper.PACKET_SIZE, socket.MSG_WAITALL).decode())
        return recv_data
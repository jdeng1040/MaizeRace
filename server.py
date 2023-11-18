import socket
import select
from _thread import *
import sys
import json
import helper

# Constants
server = "35.3.210.91"
port = 5555

class AllState:
    def __init__(self):
        # format: { name: (xPos, yPos)}
        self.locations = {}

# Create a socket to listen on
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    sys.exit(1)

# Only accept 2 connections
num_clients = 2
s.listen(num_clients)
print("Waiting for connections...Server Started")

# Initialize
game_state = AllState()

# Accept all connections for clients before beginning the game
connections = []
while True:
    client_socket, addr = s.accept()
    print("Connected to:", addr)

    connections.append(client_socket)

    if len(connections) == num_clients:
        break

# Start the game logic (No longer accept any new connections)
while True:
    # Get the list sockets which are readable
    read_sockets, write_sockets, error_sockets = select.select(connections, [], [])

    for sock in read_sockets:
        # incoming message from remote server
        data = str(sock.recv(1500).decode())
        if not data:
            print('\nDisconnected from server')
            break
        else:
            data = json.loads(data)
            print("data received", data)
            
            if data["type"] == "ENTER":
                game_state.locations[data["name"]] = (0, 0)
                if len(game_state.locations) == num_clients:
                    # everyone entered the game, we can return the maze board
                    d = helper.toJSON({
                        "type": "BEGIN",
                        "width": 10,
                        "height": 10,
                        "maze": "maze"
                    })
                    sock.sendAll(d)
                else:
                    d = helper.toJSON({
                        "type": "PLAYERS",
                        "players": list(game_state.locations.keys())
                    })
                    sock.sendall(d)
            else:
                print("unhandled TYPE")
                sys.exit(1)
            


            
            
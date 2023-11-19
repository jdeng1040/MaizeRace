import socket
import select
from _thread import *
import sys
import json
import helper
import maze

if len(sys.argv) < 2:
    print("need to give server ip")
    print(sys.argv)
    sys.exit(1)

debug_mode = "-d" in sys.argv

# Constants
server = sys.argv[1]
port = 5555


class AllState:
    def __init__(self):
        # format: { name: (xPos, yPos)}
        self.locations = {}
        self.maze_width = 25
        self.maze_height = 25
        self.maze, self.start, self.end = maze.generate_maze(self.maze_width, self.maze_height)


# Create a socket to listen on
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    listen_socket.bind((server, port))
except socket.error as e:
    str(e)
    sys.exit(1)

# Only accept 2 connections
num_clients = 2
listen_socket.listen(num_clients)
print("Waiting for connections...Server Started")

# Initialize
game_state = AllState()

# Start the game logic (No longer accept any new connections)
connections = [listen_socket]
while True:
    # Get the list sockets which are readable
    read_sockets, write_sockets, error_sockets = select.select(connections, [], [])

    for sock in read_sockets:
        if sock is listen_socket:
            # server accepting new connection
            client, _ = sock.accept()
            connections.append(client)
            continue

        data = str(sock.recv(1500, socket.MSG_WAITALL).decode())
        if not data:
            connections.remove(sock)
            sock.close()
            continue
        else:
            data = json.loads(data)
            print("data received", data)

            if data["type"] == helper.ENTER:
                game_state.locations[data["name"]] = (0, 0)
                if len(game_state.locations) == num_clients or debug_mode:
                    # everyone entered the game, we can return the maze board
                    serialized_maze = maze.serialize_maze(game_state.maze)
                    d = helper.toJSON({
                        "type": helper.BEGIN,
                        "start": game_state.start,
                        "end": game_state.end,
                        "maze": serialized_maze,
                        "players": list(game_state.locations.keys())
                    })
                    sock.sendall(d)
                else:
                    d = helper.toJSON({
                        "type": helper.PLAYERS,
                        "players": list(game_state.locations.keys())
                    })
                    sock.sendall(d)
            elif data['type'] == helper.POSITION:
                name = data["name"]
                position = data["position"]
                game_state.locations[name] = position
                d = helper.toJSON({
                    "type": helper.ALL_POSITIONS,
                    "locations": game_state.locations
                })
                sock.sendall(d)
            else:
                print("unhandled TYPE")
                sys.exit(1)

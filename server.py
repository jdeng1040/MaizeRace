import socket
import select
import sys
import json
import helper
import maze
from datetime import datetime, timedelta

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
        self.maze, self.start, self.end, self.solution = maze.generate_maze(self.maze_width, self.maze_height)
        self.maze[self.start[0]][self.start[1]] = '.'
        self.barrier_positions = []
        self.colors = {}
        for i in range(9, len(self.solution), 10):
            self.barrier_positions.append(self.solution[i])
        print("barriers:", self.barrier_positions)


# Create a socket to listen on
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    listen_socket.bind((server, port))
except socket.error as e:
    str(e)
    sys.exit(1)

# Only accept 2 connections
listen_socket.listen(helper.NUM_CLIENTS)
print("Waiting for connections...Server Started")

# Initialize
game_state = AllState()
num_finished = 0
finished = []
start_time = None

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
            # print("data received", data)

            if data["type"] == helper.ENTER:
                game_state.locations[data["name"]] = (0, 0)
                game_state.colors[data["name"]] = data["color"]
                if len(game_state.locations) == helper.NUM_CLIENTS or debug_mode:
                    # everyone entered the game, we can return the maze board
                    serialized_maze = maze.serialize_maze(game_state.maze)

                    if start_time is None:
                        start_time = datetime.now() + timedelta(seconds=4)

                    d = helper.toJSON({
                        "type": helper.BEGIN,
                        "start": game_state.start,
                        "end": game_state.end,
                        "maze": serialized_maze,
                        "players": list(game_state.locations.keys()),
                        "barriers": game_state.barrier_positions,
                        "start_time": start_time.isoformat(),
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
                    "locations": game_state.locations,
                    "colors": game_state.colors,
                })
                sock.sendall(d)
            elif data['type'] == helper.FINISH:
                name = data["name"]
                if name not in finished:
                    finished.append(name)

                f = helper.toJSON({
                        "type": helper.FINISH,
                        "rankings": finished
                    })
                sock.sendall(f)

            else:
                print("unhandled TYPE")
                sys.exit(1)

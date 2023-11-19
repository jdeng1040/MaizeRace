import json

PACKET_SIZE = 1500
# Client types sent
ENTER = "ENTER"
POSITION = "POSITION"

# Server types sent
BEGIN = "BEGIN"
PLAYERS = "PLAYERS"
ALL_POSITIONS = "ALL_POSITIONS"
FINISH = "FINISH"


def toJSON(dictionary):
    s = json.dumps(dictionary)
    if len(s) > PACKET_SIZE:
        raise ValueError("bump up size")
    else:
        s = s + " " * (PACKET_SIZE - len(s))
    return str.encode(s)

import json

PACKET_SIZE = 1500
# Client types sent
ENTER = "ENTER"

# Server types sent
BEGIN = "BEGIN"
PLAYERS = "PLAYERS"


def toJSON(dictionary):
    s = json.dumps(dictionary)
    if len(s) > PACKET_SIZE:
        raise ValueError("bump up size")
    else:
        s = s + " " * (PACKET_SIZE - len(s))
    return str.encode(s)

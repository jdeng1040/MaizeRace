import json

PACKET_SIZE = 1500

def toJSON(dictionary):
    s = json.dumps(dictionary)
    if len(s) > PACKET_SIZE:
        raise ValueError("bump up size")
    else:
        s = s + " " * (PACKET_SIZE - len(s))
    return str.encode(s)
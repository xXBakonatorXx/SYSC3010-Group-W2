import json

def to_file(data):
    with open("decoded.json", "w") as f:
        json.dump(data, f)
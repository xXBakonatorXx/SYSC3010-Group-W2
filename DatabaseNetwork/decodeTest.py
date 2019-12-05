import json

def json_to_dict(jsonfile):
    with open("decode.txt", 'r') as f:
        jsonDict = json.load(f) #load the file into our new dictionary
        print(jsonDict)
    

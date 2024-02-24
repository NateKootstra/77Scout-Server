from flask import Flask, send_file, request
from os import listdir, path
import json

server = Flask(__name__)


metadata = open("metadata.data", "r")
metadata = metadata.read().splitlines()
teamNumber = ""
serverName = ""

removed = 0
for i in range(len(metadata)):
    metadata[i - removed] = metadata[i - removed].split("=")
    
    for i2 in range(len(metadata[i - removed])):
        metadata[i - removed][i2] = metadata[i - removed][i2].strip(" ")
    
    if len(metadata[i - removed]) == 1:
        metadata.pop(i - removed)
        removed += 1
    print(metadata[i - removed][0])
    if metadata[i - removed][0] == "Team Number":
        teamNumber = metadata[i - removed][1]
    if metadata[i - removed][0] == "Server Name":
        serverName = metadata[i - removed][1]
        
        
@server.route("/name")
def return_name():
    return serverName

@server.route("/get/<team>")
def return_data(team):
    if team == teamNumber:
        data = []
        for match in listdir("matches"):
            f = open("matches/" + match, "r")
            data.append(f.read())
        return str(data)
    return "INVALID LOGIN"
        
    

@server.route("/post/<team>", methods=['GET', 'POST'])
def receive_data(team):
    if team == teamNumber:
        data = json.loads(request.data.decode())
        
        for match in data:
            if not path.exists("matches/" + match["name"] + ".json"):
                with open("matches/" + match["name"] + ".json", "w") as f:
                    json.dump(match, f)
        return "OK"
    return "INVALID LOGIN"

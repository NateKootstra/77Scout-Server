from flask import Flask, send_file, request
import os
import json

server = Flask(__name__)


metadata = open("metadata.data", "r")
metadata = metadata.read().splitlines()
teamNumber = ""
serverName = ""
scouters = []

removed = 0
for i in range(len(metadata)):
    metadata[i - removed] = metadata[i - removed].split("=")
    
    for i2 in range(len(metadata[i - removed])):
        metadata[i - removed][i2] = metadata[i - removed][i2].strip(" ")
    
    if len(metadata[i - removed]) == 1:
        metadata.pop(i - removed)
        removed += 1
    if metadata[i - removed][0] == "Team Number":
        teamNumber = metadata[i - removed][1]
    if metadata[i - removed][0] == "Server Name":
        serverName = metadata[i - removed][1]
    if metadata[i - removed][0] == "ScouterUsernames":
        scouters = metadata[i - removed][1].lstrip("[").rstrip("]").split(",")

for i in range(len(scouters)):
    scouters[i] = scouters[i].strip(" ")
    
print(scouters)

if not os.path.exists("matches"):
    os.makedirs("matches")
        
        
        
@server.route("/name")
def return_name():
    return serverName

@server.route("/get/<team>/<name>")
def return_data(team, name):
    if team == teamNumber and name in scouters:
        data = []
        for match in os.listdir("matches"):
            f = open("matches/" + match, "r")
            data.append(f.read())
        return str(data)
    return "INVALID LOGIN"
        
    

@server.route("/post/<team>/<name>", methods=['GET', 'POST'])
def receive_data(team, name):
    if team == teamNumber and name in scouters:
        data = json.loads(request.data.decode())
        for match in data:
            if not os.path.exists("matches/" + match["name"] + ".json"):
                with open("matches/" + match["name"] + ".json", "w") as f:
                    json.dump(match, f)
        return "OK"
    return "INVALID LOGIN"

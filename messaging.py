import json
import EncryptDecryptV5_0

# Notes:
# Automate each users seed based on their UID
# Automate each message seed based on MID
# Data mosh multible users pub seeds to create secure message groups
# figure out json use for DB
# 
"""User:
"0" : {
            "name": "Dean",
            "password" : "password",
            "groups" : {
                "0" : {
                    "users" : ["1"]
                }
            }
        },
"""


""" Group:
"0" : {
            "users" : ["0", "1"],
            "message_ids" : ["0"]
        }
"""


"""Message:
    "0" : "sample message"
"""

class py_json:
    def __init__(self, location):
        self.file_location = location
        self.open()

    def open(self):
        with open(self.file_location) as f:
            loaded = json.load(f)
        self.db = loaded
        self.messages = loaded["messages"]
        self.users = loaded["users"]
        self.groups = loaded["groups"]
    
    def newGroup(self):
        return self.groups["data"]["t_groups"]

    def getMessages(self, ids):
        messages = []
        for x in range(len(ids)):
            messages.insert(0, self.messages[str(ids[x])])
        return messages
    
    def addMessage(self, m):
        self.db["messages"][self.db["messages"]["data"]["t_messages"]] = m
        self.db["messages"]["data"]["t_messages"] = self.db["messages"]["data"]["t_messages"] + 1
        newData = json.dumps(self.db)
        with open(self.file_location, "w") as f:
            f.write(newData)
        return self.db["messages"]["data"]["t_messages"] - 1
        

    def updateGroup(self, group):
        self.db["groups"].pop(str(group.groupID))
        self.db["groups"][str(group.groupID)] = {
            "users" : group.users,
            "message_ids" : group.message_ids
        }
        newData = json.dumps(self.db)
        with open(self.file_location, "w") as f:
            f.write(newData)
    


class group:
    def __init__(self, groupID, users = None):
        if str(groupID) in pj.groups:
            self.groupID = groupID 
            self.message_ids = pj.groups[str(self.groupID)]["message_ids"]
            self.messages = pj.getMessages(self.message_ids)
            self.users = pj.groups[str(self.groupID)]["users"]
        else:
            self.groupID = pj.newGroup
            self.message_ids = []
            self.messages = []
            self.users = [users]

    def sendMessage(self, m):
        self.message_ids.append(pj.addMessage(m))
        pj.updateGroup(g)
        self.messages.inset(0,)
        return
        

pj = py_json("db.json")
g = group(0)


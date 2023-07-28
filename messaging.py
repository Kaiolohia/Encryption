import json
import EncryptDecryptV5_0

# Notes:
# Automate each users seed based on their UID
# Automate each message seed based on MID
# Data mosh multible users pub seeds to create secure message groups
# figure out json use for DB
# 

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

    def getMessages(self, ids:list):
        messages = []
        for x in ids:
            print(x)
            messages.insert(0, self.messages[str(x)])
        return messages
    


class group:
    def __init__(self, groupID):
        if str(groupID) in pj.groups:
            self.groupID = groupID 
            self.message_ids = pj.groups[str(self.groupID)]["message_ids"]
            self.messages = pj.getMessages(self.message_ids)
        else:
            self.groupID = pj.newGroup
            self.message_ids = []
            self.messages = []
        

pj = py_json("db.json")
g = group(0)
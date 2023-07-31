import json
import EncryptDecryptV5_0
import EvolvingSeeds

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
    
    def addUser(self, un, password):
        uid = self.db["users"]["data"]["t_users"]
        es_uid = EvolvingSeeds.ev(uid)
        ued = EncryptDecryptV5_0.EncryptDecrypt(es_uid, EncryptDecryptV5_0.seed_gen_priv(str(es_uid) + str(un)))
        n_pass = ued.encrypt_seeded(password)
        self.db["users"][str(uid)] = {
            "name": un,
            "password": n_pass,
            "groups": {}
        }
        newData = json.dumps(self.db)
        with open(self.file_location, "w") as f:
            f.write(newData)
        return [n_pass, uid, es_uid]
        

    def createGroup():
        
        return



class Group:
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

    def sendMessage(self, m, g):
        self.message_ids.append(pj.addMessage(m))
        pj.updateGroup(g)
        self.messages.insert(0,m)
        return
        
pj = py_json("db.json")

class User:    
    def __init__(self):
        self.loggedIn = False
        self.groups = []

    def login(self, username, password):
        self.username = username
        #validate password
        # pj.db["users"][str(uid)]
        found = False
        for i in range(len(pj.db["users"]) - 1):
            if username == pj.db["users"][str(i)]["name"]:
                self.uid = i
                found = True
                break
        if not found:
            raise Exception("User not found")
            return
        self.es_uid = EvolvingSeeds.ev(self.uid)
        ued = EncryptDecryptV5_0.EncryptDecrypt(self.es_uid, EncryptDecryptV5_0.seed_gen_priv(str(self.es_uid) + str(self.username)))
        if not password == ued.decrypt_seeded(pj.users[str(self.uid)]["password"]):
            raise Exception("Passwords do not match!")

        self.loggedIn = True

    def register(self, username, password):
        self.username = username
        self.password, self.uid, self.es_uid = pj.addUser(username, password)
        self.loggedIn = True

    def getDataFromDB(self):
        if self.loggedIn:
            self.userEntry = pj.users[str(self.uid)]
            # self.groups = self.userEntry["groups"]
            for i in range(len(self.userEntry["groups"])):
                self.groups.append(Group(self.userEntry["groups"][i]))

    def createGroups(self, user_ids):
        if self.loggedIn:
            return
        
    def sendMessage(self, message, group_id):
        self.groups[group_id]
u = User()


try:
    u.login("Roberts", "password")
except Exception as e:
    print(e)
import json
from EncryptDecryptV5_0 import EncryptDecrypt, seed_gen_pub, seed_gen_priv
from EvolvingSeeds import ev
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

def gen_user_seeds(username:str, uid:int):
    """
    returns a list with the public seed at index 0 and the private seed at index 1
    and the es_uid at index 2
    Es_UID = Evoling seed, User ID
    """
    es_uid = ev(uid)
    return [seed_gen_pub(es_uid), seed_gen_priv(str(es_uid) + username)]
class py_json:
    def __init__(self, location):
        """
        Args: location -> String, path to json db
        
        """
        self.file_location = location
        self.open()

    def open(self):
        """Load the json db"""
        with open(self.file_location) as f:
            loaded = json.load(f)
        self.db = loaded
        self.messages = loaded["messages"]
        self.users = loaded["users"]
        self.groups = loaded["groups"]
    
    def newGroup(self):
        """Get newest group ID"""
        return self.groups["data"]["t_groups"]

    def getMessages(self, ids):
        """Get messages by ID
        Args: ids -> list | list of message IDS
        """
        messages = []
        for x in range(len(ids)):
            messages.insert(0, self.messages[str(ids[x])])
        return messages
    
    def addMessage(self, m):
        """Add a message to the DB
        
        Args: m -> String | Message content

        Returns message ID
        """
        # self.db["messages"][self.db["messages"]["data"]["t_messages"]] = m
        self.messages[self.messages["data"]["t_messages"]] = m
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
        seeds = gen_user_seeds(un, uid)
        au_ued = EncryptDecrypt(seeds[0], seeds[1])
        n_pass = au_ued.encrypt_seeded(password)
        self.db["users"][str(uid)] = {
            "name": un,
            "password": n_pass,
            "groups": []
        }
        self.db["users"]["data"]["t_users"] = self.db["users"]["data"]["t_users"] + 1
        newData = json.dumps(self.db)
        with open(self.file_location, "w") as f:
            f.write(newData)
        
        return [n_pass, uid, seeds[2]]
        
    def updateUserGroups(self, user, groups:int):
        self.db["users"][str(user.uid)]["groups"].append(str(groups))
        newData = json.dumps(self.db)
        with open(self.file_location, "w") as f:
            f.write(newData)
        return groups

    def createGroup(self, users):
        gid = self.groups["data"]["t_groups"]
        self.db["groups"][str(gid)] = {
            "users" : users,
            "message_ids" : []
        }
        self.db["groups"]["data"]["t_groups"] = self.db["groups"]["data"]["t_groups"] + 1
        return gid



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

    def sendMessage(self, m):
        self.message_ids.append(pj.addMessage(m))
        pj.updateGroup(self)
        self.messages.insert(0,m)
        return
        
pj = py_json("db.json")

class User:    
    def __init__(self):
        self.loggedIn = False
        self.groups = {}
        self.cur_gid = None

    def login(self, username, password):
        self.username = username
        #validate password
        found = False
        for i in range(len(pj.db["users"]) - 1):
            if username == pj.db["users"][str(i)]["name"]:
                found = True
                self.uid = str(i)
                break
        if found == False:
            raise Exception("User not found")
        seeds = gen_user_seeds(self.username, self.uid)
        self.es_uid = seeds[2]
        login_ued = EncryptDecrypt(seeds[0], seeds[1])
        if not password == login_ued.decrypt_seeded(pj.users[self.uid]["password"]):
            raise Exception("Passwords do not match!")
        self.loggedIn = True
        self.getDataFromDB()

    def register(self, username, password):
        self.username = username
        self.password, self.uid, self.es_uid = pj.addUser(username, password)
        self.loggedIn = True

    def getDataFromDB(self):
        if self.loggedIn:
            self.userEntry = pj.users[str(self.uid)]
            # self.groups = self.userEntry["groups"]
            for i in range(len(self.userEntry["groups"])):
                cur_gid = self.userEntry["groups"][i]
                self.groups[cur_gid] = Group(cur_gid)

    def createGroup(self, user_ids:int):
        """Create a new group
        """
        if self.loggedIn:
            cur_gid = pj.updateUserGroups(self, pj.createGroup([str(self.uid), str(user_ids)]))
            self.groups[cur_gid] = Group(cur_gid)
            self.cur_gid = cur_gid
        
    def sendMessage(self, message):
        self.groups[str(self.cur_gid)].sendMessage(message)

    def selectGroup(self, gid):
        if str(gid) in self.groups:
            self.cur_gid = gid
        else:
            raise Exception("Group not found or not apart of the group.")
# u = User()

# try:
#     u.login("Dean", "password")
# except Exception as e:
#     print(e)

# u.selectGroup(0)
u2 = User()

u2.register("Amaya", "password")

# try:
#     u2.login("Amaya", "password")
# except Exception as e:
#     print(e)

# u2.selectGroup(0)

# u2.sendMessage("Sending a message from this user!")
# u.sendMessage("got the message above!")


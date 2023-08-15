import json
from EncryptDecryptV5_0 import EncryptDecrypt, seed_gen_pub, seed_gen_priv
from EvolvingSeeds import ev
# Notes:
# Automate each message seed based on MID
# Data mosh multible users pub seeds to create secure message groups

def gen_user_seeds(username:str, uid:int):
    """
    returns a list with the public seed at index 0 and the private seed at index 1
    and the es_uid at index 2
    Es_UID = Evoling seed, User ID
    """
    es_uid = ev(uid)
    return [seed_gen_pub(es_uid), seed_gen_priv(str(es_uid) + username), es_uid]

class Message:
    def __init__(self, raw:dict, m_id:int, a_id:int, g_id:int, encrypted:bool = False):
        """Message class is a destructed version of the raw message dictionary from the db
        EX: {"author": "2", "message": "hello"}
        """
        self.author = raw["author"]
        self.message = raw["message"]
        self.ed_key = ev(m_id + a_id + g_id)
        self.M_ED = EncryptDecrypt(seed_gen_pub(self.ed_key), seed_gen_priv(self.ed_key))
        self.__is_encrypted__ = encrypted

    def encryptMessage(self):
        if not self.__is_encrypted__:
            self.message = self.M_ED.encrypt_seeded(self.message)
            self.__is_encrypted__ = True
        return
    
    def decryptMessage(self):
        if self.__is_encrypted__:
            self.message = self.M_ED.decrypt_seeded(self.message)
            self.__is_encrypted__ = False
        return


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

    def getMessages(self, ids, groupID):
        """Get messages by ID
        Args: ids -> list | list of message IDS
        """
        messages = []
        for x in range(len(ids)):
            messageRaw = self.messages[str(ids[x])]
            messageClass = Message(messageRaw, int(ids[x]), int(messageRaw["author"]), int(groupID), True)
            messages.insert(0, messageClass)
        return messages
    
    def addMessage(self,m):
        """Add a message to the DB
        
        Args: m -> String | Message content

        Returns message ID
        """
        self.messages[str(self.messages["data"]["t_messages"])] = {
            "author" : m.author,
            "message" : m.message
        }
        self.db["messages"]["data"]["t_messages"] = self.db["messages"]["data"]["t_messages"] + 1
        newData = json.dumps(self.db, indent=4)
        with open(self.file_location, "w") as f:
            f.write(newData)
        return self.db["messages"]["data"]["t_messages"] - 1
        

    def updateGroup(self, group):
        self.db["groups"].pop(str(group.groupID))
        self.db["groups"][str(group.groupID)] = {
            "users" : group.users,
            "message_ids" : group.message_ids
        }
        newData = json.dumps(self.db, indent=4)
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
        newData = json.dumps(self.db, indent=4)
        with open(self.file_location, "w") as f:
            f.write(newData)
        
        return [n_pass, uid, seeds[2]]
        
    def updateUserGroups(self, gid):
        for uid in self.groups[str(gid)]["users"]:
            self.db["users"][uid]["groups"].append(str(gid))
        newData = json.dumps(self.db, indent=4)
        with open(self.file_location, "w") as f:
            f.write(newData)
        return gid

    def createGroup(self, users:list):
        gid = self.groups["data"]["t_groups"]
        self.db["groups"][str(gid)] = {
            "users" : users,
            "message_ids" : []
        }
        self.db["groups"]["data"]["t_groups"] = self.db["groups"]["data"]["t_groups"] + 1
        return gid
    
    def getUsernameByID(self, id):
        return self.users[str(id)]["name"]
    
    def getIDbyUsername(self, username):
        """
        Get a single user id
        """
        for i in range(len(self.users)-1):
            if self.users[str(i)]["name"] == username:
                return i
        return "User not found"
    
    def getIDbyUsernames(self, usernames):
        """
        Get a list of ids from a list of users
        """
        uids = []
        for i in range(len(self.users)-1):
            for n in usernames:
                if self.users[str(i)]["name"] == n:
                    uids.append(str(i))
        if uids == []:
            raise Exception("One or more users not found")
        return uids

class Group:
    def __init__(self, groupID, users = None):
        if str(groupID) in pj.groups:
            self.groupID = groupID 
            self.message_ids = pj.groups[str(self.groupID)]["message_ids"]
            self.messages = pj.getMessages(self.message_ids, groupID)
            self.users = pj.groups[str(self.groupID)]["users"]
        else:
            self.groupID = pj.newGroup
            self.message_ids = []
            self.messages = []
            self.users = [users]

    def sendMessage(self, author, m):
        m_id = pj.messages["data"]["t_messages"]
        newMessage = Message({"author" : author, "message" : m}, int(m_id), int(author) ,int(self.groupID))
        self.messages.insert(0, newMessage)
        newMessage.encryptMessage()
        pj.addMessage(newMessage)
        self.message_ids.append(m_id)
        pj.updateGroup(self)
        
        return
    def returnMessages(self):
        raw_messages = []
        for m in self.messages:
            raw_messages.append([m.author, m.message])
            return raw_messages
        
pj = py_json("db.json")

class User:    
    def __init__(self):
        self.__loggedIn__ = False
        self.groups = {}
        self.cur_gid = None

    def login(self, username, password):
        #validate password
        found = False
        for i in range(len(pj.db["users"]) - 1):
            if username == pj.db["users"][str(i)]["name"]:
                found = True
                self.uid = str(i)
                break
        if found == False:
            raise Exception("User not found")
        seeds = gen_user_seeds(username, self.uid)
        self.es_uid = seeds[2]
        login_ued = EncryptDecrypt(seeds[0], seeds[1])
        if not password == login_ued.decrypt_seeded(pj.users[self.uid]["password"]):
            raise Exception("Passwords do not match!")

        self.username = username
        self.__loggedIn__ = True
        self.getDataFromDB()

    def logout(self):
        if self.__loggedIn__:
            self.username = ""
            self.__loggedIn__ = False
            self.groups = {}
            self.cur_gid = None
            self.es_uid = None
            self.uid = None
            self.userEntry = None
        else:
            raise Exception("You must be logged in to logout!")
    def register(self, username, password):
        """
        str:
        Create a new account 
        """
        if self.__loggedIn__:
            raise Exception("Cannot register an account while logged in! Please log out to create a new account")
        self.username = username
        self.password, self.uid, self.es_uid = pj.addUser(username, password)
        self.__loggedIn__ = True

    def getDataFromDB(self):
        """
        Collect and process all user information
        """
        if self.__loggedIn__:
            self.userEntry = pj.users[str(self.uid)]
            for i in range(len(self.userEntry["groups"])):
                cur_gid = self.userEntry["groups"][i]
                self.groups[cur_gid] = Group(cur_gid)

    def createGroup(self, user_ids:list):
        """
        Create a new group
        """
        if self.__loggedIn__:
            user_ids.append(self.uid)
            cur_gid = pj.updateUserGroups(pj.createGroup(user_ids))
            self.groups[str(cur_gid)] = Group(cur_gid)
            self.cur_gid = cur_gid
        
    def sendMessage(self, message):
        """
        str: message
        Need to have a group selected to send a message
        sends a message to a group
        """
        self.groups[str(self.cur_gid)].sendMessage(self.uid, message)

    def selectGroup(self, gid):
        """
        Select what group the user is currently in.
        Need to be in a valid group to utilize certain functions
        """
        if str(gid) in self.groups:
            self.cur_gid = gid
        else:
            raise Exception("Group not found or not apart of the group.")
    def logout(self):
        """
        Clears all instance data
        """
        self.__loggedIn__ = False
        self.groups = {}
        self.cur_gid = None
        self.es_uid = None
        self.username = None
        self.userEntry = None
        return "Successfully Logged out!"
    
    def formatMessage(self, message):
        """Converts each message class to a dictionary with the author name and the decrypted message"""
        message.decryptMessage()
        return {"author": pj.getUsernameByID(message.author), "message": message.message}
    def getMessages(self):
        """Collect all messages within a group and format them on the client side for readability"""
        messages = []
        for m in self.groups[str(self.cur_gid)].messages:
            messages.append(self.formatMessage(m))
        return messages

    def isLoggedIn(self):
        """Expose data of logged in status without the ability to change the status manually"""
        return self.__loggedIn__
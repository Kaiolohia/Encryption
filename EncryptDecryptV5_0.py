import random
import string
import base62

class EncryptDecrypt():
    """
    EncryptDecrypt has two seeds which can be generated each by using seed_gen_pub() for the public key and seed_gen_priv() for the private key
    The public key is just a string of numbers ran trough base62
    """

    def __init__(self, 
    public_seed:str = "123456789", 
    private_seed:str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ"):
        """
        Takes in seeds and destructures them
        """
        self.public_seed = base62.decode(public_seed) if public_seed != "123456789" else "123456789"
        self.private_seed = "".join(from_number(str(private_seed))) if private_seed != "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ" else "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ"
        destructured_seed = self.destructure_priv_seed()
        self.seed_2 = list(destructured_seed[1])
        self.seed_3 = list(destructured_seed[0])
        self.s_b62 = base62.seeded(destructured_seed[2])

    def destructure_priv_seed(self):
        """
        The private seed comes in as one big key with three sub keys
        """
        return [self.private_seed[0:10], self.private_seed[10:61], self.private_seed[62:]]
        

    def encrypt(self, msg): #unseeded encryption, leaves tools to decrypt in the message
        """
        This encrypt method takes our message and adds to its ascii value by two other
        chars that is randomly picked, our message is now a long int, so we run it through my own number
        encryption method down below. Lastly we send that int through custom base62 for both storage
        friendly ness and also another layer of security.
        """
        msg = to_number(msg)
        letter_map = []
        char_choices = string.ascii_letters
        #For each charecter in our message we convert it into an ascii int then add its value
        #by two other chars in the form as ints.
        for i in range(len(msg)):
            char1 = random.choice(char_choices)
            char2 = random.choice(char_choices)
            msg[i] = str(int(msg[i]) + ord(char1) + ord(char2)).zfill(3)
            letter_map.insert(i,str(ord(char1)).zfill(3))
            letter_map.append(str(ord(char2)).zfill(3))
        msg[0] = str(int(msg[0]) + 200)
        return base62.encode(int(''.join(numbers_encrypt("".join(msg + letter_map)))))
    
    def encrypt_seeded(self, msg):
        """
        Just like the unseeded version, we do similar things in the seeded version
        But the difference here is that there isnt a clue left in the final message
        that will lead to the decryption of the message without seeds.
        Instead of pure random-ness it is seeded before hand. We also seed the base62 and
        the numbers encryption.
        """
        msg = to_number(msg)
        letter_map = []
        random.seed(self.public_seed)
        choices = self.seed_2[:]
        random.shuffle(choices)
        for i in range(len(msg)):
            char1 = random.choice(choices)
            char2 = random.choice(choices)
            msg[i] = str(int(msg[i]) + ord(char1) + ord(char2)).zfill(3)
        msg[0] = str(int(msg[0]) + 200)
        return self.s_b62.encode(int(''.join(numbers_encrypt("".join(msg)))))

    def decrypt(self, msg):
        """
        Reads the clues left in the message for how much to adjust the message by
        the encrypted method. Then we do the steps in reverse.
        """
        msg = ascii_chunk(numbers_decrypt(list(str(base62.decode(msg)))))
        msg[0] = str(int(msg[0]) - 200).zfill(3)
        #descructuring
        des_msg = msg[0:int(len(msg)/3)]
        letter_map = msg[int(len(msg)/3):]
        letter_map_1 = letter_map[0:int(len(letter_map)/2)]
        letter_map_2 = letter_map[int(len(letter_map)/2):]
        #decrypting
        for i in range(len(des_msg)):
            des_msg[i] = chr(int(des_msg[i]) - int(letter_map_1[i]) - int(letter_map_2[i]))
        return "".join(des_msg)

    def decrypt_seeded(self, msg):
        """
        This method does the same as the normal decrypt but we add our keys.
        """
        msg = ascii_chunk(numbers_decrypt(list(str(self.s_b62.decode(msg)))))
        msg[0] = str(int(msg[0]) - 200).zfill(3)
        #decrypting
        random.seed(self.public_seed)
        choices = self.seed_2[:]
        random.shuffle(choices)
        for i in range(len(msg)):
            char1 = ord(random.choice(choices))
            char2 = ord(random.choice(choices))
            msg[i] = chr(int(msg[i]) - int(char1) - int(char2))
        return "".join(msg)

def numbers_encrypt(msg, seed = [0,1,2,3,4,5,6,7,8,9]):
    """
    Encrypts numbers by pulling their index from scramble array
    then replacing them in the message.
    the scramble array for encryption gets shifted from right to left every iteration/check
    IE iteration 0 // 0,1,2,3,4,5,6,7,8,9
        iteration 1 // 1,2,3,4,5,6,7,8,9,0
        iteration2 // 2,3,4,5,6,7,8,9,0,1
    """
    scramble_array = seed[:]
    msg = list(msg)
    new_msg = []
    for c in list("".join(msg)):
        scramble_array.append(scramble_array.pop(0))
        try:
            new_msg.append(str(scramble_array.index(int(c))))
        except:
            print(c)
            raise

    return new_msg

def numbers_decrypt(msg:list, seed = [0,1,2,3,4,5,6,7,8,9]):
    """
    Decrypts numbers by pulling their index from scramble array
    then replacing them in the message.
    the scramble array for encryption gets shifted from left to right every iteration/check
    IE iteration 0 // 0,1,2,3,4,5,6,7,8,9
    iteration 1 // 9,0,1,2,3,4,5,6,7,8
    """
    scramble_array = seed[:]
    new_msg = []
    for c in msg:
        scramble_array = scramble_array[-1:] + scramble_array[:-1]
        if c.isdigit():
            new_msg.append(str(scramble_array.index(int(c))))
        else:
            new_msg.append(c)
    return new_msg

def to_number(msg):
    """
    Converts a long message into a list of ascii ints
    """
    nums = []
    for c in msg:
        nums.append(str(ord(c)).zfill(3))
    return nums

def from_number(msg):
    """
    Converts an INT of ascii chars from int form to char form.
    """
    nums = []
    chunk = ''
    for i in range(1, len(msg) + 1):
        if i%3 == 0:
            chunk += msg[i-1]
            nums.append(str(chr(int(chunk))))
            chunk = ''
        else:
            chunk += msg[i-1]
    return nums

def ascii_chunk(input:str):
    """
    Ascii int's are three digits long
    This function converts a long int into chunks of three
    """
    chunks = []
    for i in range(0, len(input), 3):
        chunks.append("".join(input[i:i+3]))
    return chunks

def seed_gen_pub(seed = None):
    """
    Generates a seed that fits the public key format
    Repeatable outcome based on seed
    """
    random.seed(seed)
    res = random.randint(1,10**6021)
    return base62.encode(res)

def seed_gen_priv(seed):
    """
    Generates a public seed that fits the format of the private key
    """
    random.seed(seed)
    nums = ["0","1","2","3","4","5","6","7","8","9"]
    letters = list(string.ascii_letters)
    seed = ""
    
    random.shuffle(nums)
    seed += "".join(nums)

    random.shuffle(letters)
    seed += "".join(letters)

    random.shuffle(nums)
    random.shuffle(letters)
    seed += "".join(nums) + "".join(letters)
    return "".join(to_number(seed))
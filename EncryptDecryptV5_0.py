import random
import string
import base62

"""
(IDEA): Get value of seed and random letters and then manipulate the message int from there intead of only from random letters and leaving the seed useless
"""
"""
(IDEA): Two versions of encrypt and decrypt, one is seeded and the other is not, seeded one leaves no data
"""
"""
(IDEA): two seeds but the second one is a large seed that has all 3 private seeds in it
"""

class EncryptDecrypt():
    '''
    EncryptDecrypt takes in 3 optional seeds, seed_1 is your "main" seed
    seed_2 is your alphabetical seed, this takes in a list of UPPER AND LOWERCASE letters from the english alphabet
    in any order ["x", "s", "t"...]
    seed_3 is your numerical seed, this takes a list of numbers 0-9 in any order [5,1,2...]
    '''

    def __init__(self, 
    public_seed:str = "123456789", 
    private_seed:str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ"):
        self.public_seed = base62.decode(public_seed) if public_seed != "123456789" else "123456789"
        self.private_seed = "".join(from_number(str(private_seed))) if private_seed != "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ" else "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ"
        destructured_seed = self.destructure_priv_seed()
        self.seed_2 = list(destructured_seed[1])
        self.seed_3 = list(destructured_seed[0])

    def destructure_priv_seed(self):
        destructure = []
        destructure.append(self.private_seed[0:10])
        destructure.append(self.private_seed[10:61])
        destructure.append(self.private_seed[61:])
        return destructure
        

    def encrypt(self, msg): #unseeded encryption, leaves tools to decrypt in the message
        msg = to_number(msg)
        letter_map = []
        char_choices = string.ascii_letters
        for i in range(len(msg)):
            char1 = random.choice(char_choices)
            char2 = random.choice(char_choices)
            msg[i] = str(int(msg[i]) + ord(char1) + ord(char2)).zfill(3)
            letter_map.insert(i,str(ord(char1)).zfill(3))
            letter_map.append(str(ord(char2)).zfill(3))
        msg[0] = str(int(msg[0]) + 200)
        return base62.encode(int(''.join(numbers_encrypt("".join(msg + letter_map)))))
    
    def encrypt_seeded(self, msg):
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
        return base62.encode(int(''.join(numbers_encrypt("".join(msg)))))

    def decrypt(self, msg):
        """
        Decrypts unseeded encryptions
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
        msg = ascii_chunk(numbers_decrypt(list(str(base62.decode(msg)))))
        msg[0] = str(int(msg[0]) - 200).zfill(3)
        #decrypting
        random.seed(self.public_seed)
        choices = self.seed_2[:]
        random.shuffle(choices)
        for i in range(len(msg)):
            char1 = random.choice(choices)
            char2 = random.choice(choices)
            msg[i] = chr(int(msg[i]) - int(ord(char1)) - int(ord(char2)))
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
    for char in list("".join(msg)):
        scramble_array.append(scramble_array.pop(0))
        try:
            new_msg.append(str(scramble_array.index(int(char))))
        except:
            print(char)
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
    for char in msg:
        scramble_array = scramble_array[-1:] + scramble_array[:-1]
        if char.isdigit():
            new_msg.append(str(scramble_array.index(int(char))))
        else:
            new_msg.append(char)
    return new_msg

def to_number(msg):
    nums = []
    for char in msg:
        nums.append(str(ord(char)).zfill(3))
    return nums

def from_number(msg):
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
    chunks = []
    for i in range(0, len(input), 3):
        chunks.append("".join(input[i:i+3]))
    return chunks

def seed_gen_pub():
    seed = random.randint(1,10**6021)
    return base62.encode(seed)

def seed_gen_priv():
    random.seed()
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
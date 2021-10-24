"""
::::::::::::::::Welcome to EncryptDecryptV4_A::::::::::::::::
:::::::::::::::::::::::::Trux#0001:::::::::::::::::::::::::::
Change log from V3_0:
  Added encrypted message to bytes -> encrypted bytes
  
  What V4_A now does is the V3_0 encryption and converts that
    into a binary string, then to hide the fact that its binary
    I use a number switch map that swaps the inputed number
    to the found index of a list of nums 1-9, because
    I am using binary there is a pattern if you leave the map list
    just as 1,2,3 etc where it slowy goes down (99875432100976653)
    {no number is more than 2 digits from the other}
    As a remedy to this you should use a custom map of similar length
    of random order, (3,2,7,1,9,0,4,5,6,8) for example.

  Other notes:
    :::::THIS IS NOT STORAGE FRIENDLY:::::
      Each final message comes out to be ~32 times larger
      (working on converting binary to hex to fix this in a later
      version)
      I do believe that this is a very secure method so long as 
      the method is kept private
      Knowing how it works means knowing how to solve it.

"""



import random
import base64

#These are the encryption maps used to swap around letters and also to put the shift iteration keys before each letter

class EncryptDecrypt:
  swapDict = {'a':'b','b':'c','c':'d','d':'e','e':'f','f':'g','g':'h','h':'i','i':'j','j':'k','k':'l','l':'m','m':'n','n':'o','o':'p','p':'q','q':'r','r':'s','s':'t','t':'u','u':'v','v':'w','w':'x','x':'y','y':'z','z':'a', ' ':' ', 'A':'B','B':'C','C':'D','D':'E','E':'F','F':'G','G':'H','H':'I','I':'J','J':'K','K':'L','L':'M','M':'N','N':'O','O':'P','P':'Q','Q':'R','R':'S','S':'T','T':'U','U':'V','V':'W','W':'X','X':'Y','Y':'Z','Z':'A', '.':',',',':'?', '?':'/', '/':'\'', '\'':'|', '|':':', ':': '(', '(':')', ')':'"', '"':'@', '@':'$', '$':'%', '%':'<', '<': '>', '>':'^', '^':'[', '[':']', ']':'{', '{':'}', '}':'+', '+':'-', '-':'=', '=':'_', '_':'&', '&':'*', '*':'.', '`':'`', '#':'#', '!':'!', '\\':'\\', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9', '0':'0'}
  alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
  Mainseed = 69420
  def __init__(self,seed = 69420): #V3.0 now includes manual seed injection instead of a set one in the file. You now declare EncryptDecrypt as a class varible with your own seed to use this.
    self.Mainseed = seed
  
  def encrypt(self,input):
    random.seed(self.Mainseed)
    Alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    random.shuffle(Alphabet)
    iterationInt = random.randint(1,26)
    splitInput = list(input)
    encryptedWord = ''
    encryptedLetter = []
    iterationMap = []

    #Creation of the seed, we take in the input and make that the seed but then we hide the seed later on. This section is prepping it to be added
    seed = random.randint(10**(len(splitInput)-1), 10**(len(splitInput)))
    random.seed(str(seed))
    
    #using our seed from before we shuffle the alphabet around and make that our iteration map key and value dictionary
    
    iterationDict = {}
    TempAlphabet = Alphabet[:]
    random.shuffle(TempAlphabet)
    random.seed()
    for x in range(26):
      iterationDict[x+1] = TempAlphabet[x]
    iterationDictReader = {value : key for (key, value) in iterationDict.items()}

    #individual iteration map
    #This simply creates a map of equal length to the message with letters from iterationDict to be spliced and placed before each letter
    for _ in range(len(splitInput)):
      iterationMap.append(iterationDict[random.randint(1,9)])

    #This is the first layer of encryption, the second loop reads how many times it needs to shift each letter based on the iteration map 
    #then then updates the message with the new chars
    for e in range(len(splitInput)):
      for a in range(iterationDictReader[iterationMap[e]]):
        splitInput[e] = self.swapDict[splitInput[e]]
    inputLength = len(splitInput)

    #This next loop places a charector of the iteration map infront of each charector of the message
    for x in range(inputLength):
      splitInput.insert(x*2,iterationMap[x])


    #this is the second layer of encryption. We do a very similar step to the first layer except now we encrypt the entire message again to a new shift amount
    #And also adding its shift key to the very front
    for _ in range(iterationInt):
      for letter in range(len(splitInput)):
        encryptedLetter.append(self.swapDict[splitInput[letter]])
      splitInput = encryptedLetter[:]
      encryptedLetter.clear()

    #here we add our seed to every third value making our encrypted message me layed out as such {(main Iterator),(seedN),(iterator),(letter),(seedN),(iterator),(Letter),etc}
    seed = list(str(seed))
    for x in range(inputLength):
        splitInput.insert(x*3,seed[x])


    #Throw in message map key in the beggining
    encryptedWord += iterationDict[iterationInt]
    # for b in range(len(splitInput)):
    #   encryptedWord = encryptedWord + splitInput[b]
    splitInput.insert(0, encryptedWord)
    encryptedWord = ''.join(numbers_encrypt(to_bytes(splitInput)))
    
    #Lastly we encode our message in base 64 and send it off to where ever it needs to go, I choose to do this step because when you initially want to decrypt any of my messsages
    #Anyone with enough competence can see that its in base64, however when you decode it, it looks like jibberish which in turn hopefully deroutes any attacker
    #This base64 addition does not add to the security nor do I count it as part of my possible combination count.
    encryptedWord = base64.b64encode(''.join(encryptedWord).encode('ascii')).decode('ascii')
    return encryptedWord


  def decrypt(self,input):
    random.seed(self.Mainseed)
    Alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    random.shuffle(Alphabet)
    input = base64.b64decode(input.encode('ascii')).decode('ascii')
    splitInput = list(from_bytes(''.join(numbers_decrypt(input))))
    decryptedLetter = []
    decryptedWord = ''
    iterationMap = []
    firstChar = splitInput.pop(0)
    seedExtractionList = splitInput[:]
    seed = []
    
    #Extracting the seed from the message
    for x in range(len(seedExtractionList)):
      try:
        seed.append(seedExtractionList.pop(x))
        seedExtractionList.pop(x)
      except:
        break
    seed = ''.join(seed)

    #Same iteration Map creation as before, now that the seed is extracted, creating the map to decrypt the message is possible
    splitInput.insert(0, firstChar)
    iterationDict = {}
    random.seed()
    random.seed(seed)
    TempAlphabet = Alphabet[:]
    random.shuffle(TempAlphabet)
    for x in range(26):
      iterationDict[x+1] = TempAlphabet[x]
    iterationDictReader = {value : key for (key, value) in iterationDict.items()}
    #From our encrypt steps we work backwards, because there are 26 letters in the english alphabet we iterate through the entire alphabet minus the iteration key amount to return
    #to our original message before the second layer of encryption (i.e. Before we iterate the entire message)
    for _ in range(26 - iterationDictReader[splitInput[0]]):
      for letter in range(len(splitInput)):
        decryptedLetter.append(self.swapDict[splitInput[letter]])
      splitInput = decryptedLetter[:]
      decryptedLetter.clear()
    splitInput.pop(0)
    
    #We remove the seed from the message
    for x in range(len(splitInput)):
      try:
        if x % 2 == 0:
          splitInput.pop(x)
      except:
        break

    
    #this now cleans our message and maps out our iteration reader to decrypt each individual letter
    tempLength = len(splitInput)
    for var in range(tempLength):
      if (tempLength/2 == var):
        break
      iterationMap.append(splitInput.pop(var))
      
    
    #Next loop does what the first one does but for each letter, bringing us back to before our first layer of encryption
    for e in range(len(splitInput)):
      for a in range(26 - iterationDictReader[iterationMap[e]]):
        splitInput[e] = self.swapDict[splitInput[e]]

    
    #Lastly we convert our decrypted list of charectors back to a readable string
    for b in range(len(splitInput)):
      decryptedWord = decryptedWord + splitInput[b]
    return decryptedWord

def numbers_encrypt(msg, scramble_array = [0,1,2,3,4,5,6,7,8,9]):
  """
  Encrypts numbers by pulling their index from scramble array
  then replacing them in the message.
  the scramble array for encryption gets shifted from right to left every iteration/check
  IE iteration 0 // 0,1,2,3,4,5,6,7,8,9
    iteration 1 // 1,2,3,4,5,6,7,8,9,0
  """
  msg = list(msg)
  new_msg = []
  for char in list("".join(msg)):
    scramble_array.append(scramble_array.pop(0))
    new_msg.append(str(scramble_array.index(int(char))))
  return new_msg

def numbers_decrypt(msg:list):
  """
  Decrypts numbers by pulling their index from scramble array
  then replacing them in the message.
  the scramble array for encryption gets shifted from left to right every iteration/check
  IE iteration 0 // 0,1,2,3,4,5,6,7,8,9
    iteration 1 // 9,0,1,2,3,4,5,6,7,8
  """
  scramble_array = [0,1,2,3,4,5,6,7,8,9]
  new_msg = []
  for char in msg:
    scramble_array = scramble_array[-1:] + scramble_array[:-1]
    if char.isdigit():
      new_msg.append(str(scramble_array.index(int(char))))
    else:
      new_msg.append(char)
  return new_msg

def to_bytes(msg):
  """
  
  """
  nums = []
  for char in msg:
    nums.append(format(ord(char), "008b"))
  return nums

def from_bytes(msg):
  nums = []
  byte = ''
  for i in range(1, len(msg) + 1):
    if i%8 == 0:
      byte += msg[i-1]
      nums.append(str(chr(int(byte,2))))
      byte = ''
    else:
      byte += msg[i-1]
  return nums
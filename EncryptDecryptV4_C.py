"""
::::::::::::::::Welcome to EncryptDecryptV4_B::::::::::::::::
:::::::::::::::::::::::::Trux#0001:::::::::::::::::::::::::::
  Whats different from v4_B? Security, and space.
    V4_C Provides the same encryption method as v3_0 but it includes
    the number encryption as V4_A and B. Making it the same 
    space efficiency as V3_0 with another layer of security.
    Just not as much security as A or B.
"""
"""
Visualized:
Message = "Test"

Message gets its length captured (4)
then we make a seed based on its length using some funky math for
the random library to get us a number for each char based on length in one pass
Random Integer ((10^ (length of message {4}) -1), ((10^ (length of message {4}))

Then we make a dictionary based on a randomized alphabet with indexes for
quick calling of the number: letter pair seed

Next we make a "iteration Map" of equal length to our message
This map will tell us by letter how many times we shift our letter through the randomized alphabet

Then we shift the letters based on the map however many times the map says
```
IterationMap = ["b", "e", "y", "q"]
IteraionDictReader = {"b":1, "e":2, "y":3, "q":4} #This is an example, the amount is normally randomized
"Test" -> "bUegyvqx" You can spot our IterationMap in every odd position inside of our new message
Message = "bUegyvqx"
```
Next we add another layer onto our message using realtively the same method
This time we shift the entire message by a single random amount instead of each letter
{a:1}
"bUegyvqx" -> "cVfhzwry"

Then we import our seed for decryption right into the message itself
lets say:
seed = 1234
```
"cVfhzwry" -> "cV1fh2zw3ry4" 
```

Then we add on our entire message iteration key from two steps back
"cV1fh2zw3ry4" ->"acV1fh2zw3ry4"

Almost finished, next we run out message through a number encryption (see numbers_encrypt() docstring)
"acV1fh2zw3ry4" -> "acV8fh4zw0ry5"

Lastly we send it through a Base64 encoder as a fake route. If you see a B64 string that decodes into
acV8fh4zw0ry5 your first instinct is most likely "its not base 64 let me try something else"
"acV8fh4zw0ry5" -> "YWNWOGZoNHp3MHJ5NQ="
This does not provide real protection if someone is dedicated enough as anyone can decode B64.
It is done to fake a malicious person down a "rabbit hole" that wont get them anywhere without
the right knowledge
"""
"""
Decryption is the exact same process other than the seed extraction, other than that go up the steps and do everything backwards
EXCEPT for the letter shifting part, that you will have to do (26-shift index) that way you loop through
the alphabet and return back to your original letter rather than a letter down the line.

Decryption for numbers is in the numbers_decrypt() docstring
"""

import random
import base64
import Includes
import time

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
    encryptedWord = ''.join(numbers_encrypt(splitInput))
    
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
    splitInput = list(''.join(numbers_decrypt(input)))
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

def numbers_encrypt(msg):
  """
  Encrypts numbers by pulling their index from scramble array
  then replacing them in the message.
  the scramble array for encryption gets shifted from right to left every iteration/check
  IE iteration 0 // 0,1,2,3,4,5,6,7,8,9
    iteration 1 // 1,2,3,4,5,6,7,8,9,0
  """
  
  msg = list(msg)
  scramble_array = [0,1,2,3,4,5,6,7,8,9]
  new_msg = []
  for char in list("".join(msg)):
    scramble_array.append(scramble_array.pop(0))
    if str(char).isdigit():
      new_msg.append(str(scramble_array.index(int(char))))
    else:
      new_msg.append(str(char))
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


if __name__ == '__main__':
  # Includes.LoadingScreen()
  ValidInput = False
  while not ValidInput:
    Includes.Clear()
    cur_input = input('Encrypt or Decrypt: ').lower()
    if cur_input == 'encrypt':
        print(EncryptDecrypt.encrypt(EncryptDecrypt,input('Encrypt: ')))
        ValidInput = True
        break
    elif cur_input== 'decrypt':
        print(EncryptDecrypt.decrypt(EncryptDecrypt,input('Decrpyt: ')))
        ValidInput = True
        break
    else:
        print('Invalid Input | Please type either Encrypt or Decrypt')
        time.sleep(1)
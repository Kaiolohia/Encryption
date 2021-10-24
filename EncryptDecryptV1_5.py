#=-=-=-=-=-=-=-=-=-=-=-=-=Encrypt-Decrypyt-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#                          By-Trux#0001                                 #
#                                                                       #
# Important notes:                                                      #
#                 This is a custom encrypt and decrypt method           #
#                 developed by me. It doesnt provide space              #
#                 optimization at all (doubles your message length).    #
#                 It also hasnt been tested to see how effective        #
#                 this method is.                                       #
#                                                                       #
#                  And heres the math...                                #
#                     Each letter can have 26 combinations.             #
#                                                                       #
#                     Unfortunately numbers do not get encrypted        #
#                                                                       #
#                     Each message can have 26 combinations             #
#                                                                       #
#                     Theoretically, with the amount of supported       #
#                     charectors each message has the math of           #
#                     60164 x (amount of charectors) = Combinations     #
#                                                                       #
#                     (60164 coming from 89 supported charectors times  #
#                      26 combinations per charector, times 26          #
#                      combinations per message)                        # 
#                                                                       #
#        (This info section alone has 87 Million Combinations!!!)       # 
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#



import random
import base64

#These are the encryption maps used to swap around letters and also to put the shift iteration keys before each letter
swapDict = {'a':'b','b':'c','c':'d','d':'e','e':'f','f':'g','g':'h','h':'i','i':'j','j':'k','k':'l','l':'m','m':'n','n':'o','o':'p','p':'q','q':'r','r':'s','s':'t','t':'u','u':'v','v':'w','w':'x','x':'y','y':'z','z':'a', ' ':' ', 'A':'B','B':'C','C':'D','D':'E','E':'F','F':'G','G':'H','H':'I','I':'J','J':'K','K':'L','L':'M','M':'N','N':'O','O':'P','P':'Q','Q':'R','R':'S','S':'T','T':'U','U':'V','V':'W','W':'X','X':'Y','Y':'Z','Z':'A', '.':',',',':'?', '?':'/', '/':'\'', '\'':'|', '|':':', ':': '(', '(':')', ')':'"', '"':'@', '@':'$', '$':'%', '%':'<', '<': '>', '>':'^', '^':'[', '[':']', ']':'{', '{':'}', '}':'+', '+':'-', '-':'=', '=':'_', '_':'&', '&':'*', '*':'.', '`':'`', '#':'#', '!':'!', '\\':'\\', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9', '0':'0'}

def encrypt(input):
  iterationInt = random.randint(1,26)
  splitInput = list(input)
  encryptedWord = ''
  encryptedLetter = []
  iterationMap = []
  seedList = splitInput[:]
  seedList.reverse()
  seed = []


  #Creation of the seed, we take in the input and make that the seed but then we hide the seed later on. This section is prepping it to be added
  for x in range(len(splitInput)):
    seed.append(swapDict[seedList[x]])
  seed = ''.join(seed)
  random.seed(input)
  
  
  #using our seed from before we shuffle the alphabet around and make that our iteration map key and value dictionary
  alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
  iterationDict = {}
  random.shuffle(alphabet)
  random.seed()
  for x in range(26):
    iterationDict[x+1] = alphabet[x]
  iterationDictReader = {value : key for (key, value) in iterationDict.items()}

  #individual iteration map
  #This simply creates a map of equal length to the message with letters from iterationDict to be spliced and placed before each letter
  for _ in range(len(splitInput)):
    iterationMap.append(iterationDict[random.randint(1,9)])

  #This is the first layer of encryption, the second loop reads how many times it needs to shift each letter based on the iteration map then then updates the message with the new chars
  for e in range(len(splitInput)):
    for a in range(iterationDictReader[iterationMap[e]]):
      splitInput[e] = swapDict[splitInput[e]]
  inputLength = len(splitInput)

  #This next loop places a charector of the iteration map infront of each charector of the message
  for x in range(inputLength):
    splitInput.insert(x*2,iterationMap[x])


  #this is the second layer of encryption. We do a very similar step to the first layer except now we encrypt the entire message again to a new shift amount
  #And also adding its shift key to the very front
  for _ in range(iterationInt):
    for letter in range(len(splitInput)):
      encryptedLetter.append(swapDict[splitInput[letter]])
    splitInput = encryptedLetter[:]
    encryptedLetter.clear()

  #here we add our seed to every third value making our encrypted message me layed out as such {(main Iterator),(seedN),(iterator),(letter),(seedN),(iterator),(Letter),etc}
  for x in range(inputLength):
      splitInput.insert(x*3,seed[x])


  #This next section formats the message from a list of charectors to a string
  encryptedWord += iterationDict[iterationInt]
  for b in range(len(splitInput)):
    encryptedWord = encryptedWord + splitInput[b]

  #Lastly we encode our message in base 64 and send it off to where ever it needs to go, I choose to do this step because when you initially want to decrypt any of my messsages
  #Anyone with enough competence can see that its in base64, however when you decode it, it looks like jibberish which in turn hopefully deroutes any attacker
  encryptedWord = base64.b64encode(encryptedWord.encode('ascii')).decode('ascii')
  return encryptedWord


def decrypt(input):
  input = base64.b64decode(input.encode('ascii')).decode('ascii')
  splitInput = list(input)
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
  seed.reverse() #I shove the seed in reverse in the message so we revert it back to normal here
  for _ in range(25): #Because I only iterate the seed once we loop throught the swapDict 25 times to get back to normal
    for x in range(len(seed)):
      seed[x] = swapDict[seed[x]]
  seed = ''.join(seed)


  #Same iteration Map creation as before, now that the seed is extracted, creating the map to decrypt the message is possible
  splitInput.insert(0, firstChar)
  alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
  iterationDict = {}
  random.seed(seed)
  random.shuffle(alphabet)
  random.seed()
  for x in range(26):
    iterationDict[x+1] = alphabet[x]
  iterationDictReader = {value : key for (key, value) in iterationDict.items()}
  #From our encrypt steps we work backwards, because there are 26 letters in the english alphabet we iterate through the entire alphabet minus the iteration key amount to return
  #to our original message before the second layer of encryption (i.e. Before we iterate the entire message)
  for _ in range(26 - iterationDictReader[splitInput[0]]):
    for letter in range(len(splitInput)):
      decryptedLetter.append(swapDict[splitInput[letter]])
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
      splitInput[e] = swapDict[splitInput[e]]

  
  #Lastly we convert our decrypted list of charectors back to a readable string
  for b in range(len(splitInput)):
    decryptedWord = decryptedWord + splitInput[b]
  return decryptedWord


#Self explanitory
if __name__ == '__main__':
    cur_input = input('Encrypt or Decrypt: ').lower()
    if cur_input == 'encrypt':
        print(encrypt(input('Encrypt: ')))
    elif cur_input== 'decrypt':
        print(decrypt(input('Decrpyt: ')))
    else:
        print('Invalid Input | Please type either Encrypt or Decrypt')
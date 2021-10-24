import time
import EncryptDecryptV2_0
from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def encrypt(input):
    toBeEncrypted = ''
    input = list(input)
    for x in range(len(input)):
        progress = int(x / len(input) * 10)
        toBeEncrypted = toBeEncrypted + input[x]
        print('Encrypting: ' + u'\u2588' * progress + '_' * (10 - progress))
        print(EncryptDecryptV2_0.encrypt(toBeEncrypted))
        time.sleep(0.05)
        clear()
    print('Encrypted: ' + u'\u2588' * 10)
    print(EncryptDecryptV2_0.encrypt(toBeEncrypted))

def decrypt(input):
    initalDecrypt = EncryptDecryptV2_0.decrypt(input)
    initalDecrypt = list(initalDecrypt)
    backUpDecrypt = initalDecrypt[:]
    toBePrinted = ''
    for x in range(len(initalDecrypt)):
        progress = int(x / len(backUpDecrypt) * 10)
        toBeDecrypted = ''
        toBePrinted += backUpDecrypt[x]

        initalDecrypt.pop()
        toBeDecrypted = toBeDecrypted.join(initalDecrypt)
        print('Decrypting: ' + u'\u2588' * progress + '_' * (10 - progress))
        print(EncryptDecryptV2_0.encrypt(toBeDecrypted))
        print(f'Decrypted Message: {toBePrinted}')
        time.sleep(0.05)
        clear()
    print('Decrypted: ' + u'\u2588' * 10)
    print(f'Your message: {toBePrinted}')

encrypt(input('Encrypt: '))
decrypt(input('Decrypt: '))



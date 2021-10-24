from EncryptDecryptV4_B import numbers_encrypt, to_number 

#import seed from DB and place it into var idx

idx = 1

for x in range(10000):
    print("".join(to_number(numbers_encrypt(str(x), [1,7,2,8,3,9,4,6,5,0]))))
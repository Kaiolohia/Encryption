from EncryptDecryptV5_0 import numbers_encrypt, to_number

"""
Evolving seeds is the concept of taking an index from a data base and making a set seed based on it
such as idx = 1 -> 156781
"""

def ev(x):
    # double encrypt seed (x) and multiplies it by base_num to get a "hash" version of x that is repeatable
    base_num = 1248133254781654
    return "".join(numbers_encrypt(numbers_encrypt(str(int(x) * base_num), [1,7,2,8,3,9,4,6,5,0]), [1,7,2,8,3,9,4,6,5,0]))
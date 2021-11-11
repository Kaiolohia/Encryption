import EncryptDecryptV5_0
import EncryptDecryptV4_A
import EncryptDecryptV4_B
import EncryptDecryptV4_C
import EncryptDecryptV3_0
import EncryptDecryptV2_0
import EncryptDecryptV1_0
import time
iterations = 100000
edV_5 = EncryptDecryptV5_0.EncryptDecrypt()
edV4_A = EncryptDecryptV4_A.EncryptDecrypt()
edV4_B = EncryptDecryptV4_B.EncryptDecrypt()
edV4_C = EncryptDecryptV4_C.EncryptDecrypt()
edV3 = EncryptDecryptV3_0.EncryptDecrypt()


#all of the decrypt tasks are each versions output of "Sample"
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end_time = time.time() - start
        print(f"Time elapsed for {func.__name__}: {end_time}s | Iterations: {iterations}")
        return res
    return wrapper

@timer
def decrypt_v5():
    for i in range(iterations):
        edV_5.decrypt("lPxyBPxFqS9QQKqZJeIORXELXVqyqD")

@timer
def decrypt_v4_A():
    for i in range(iterations):
        edV4_A.decrypt("OTk4NzU1NDMxMDA5Nzc1NTMzMjE5OTg3NTUzMzEwOTg3NjY1NDIxMDk5ODc1NTMyMTEwOTg2NTUzMjIxMDg3NjU1NDMxMTk5Nzc2NDQzMTA5ODg3NTUzMjExMDk4NjY0MzMyMDA4Nzc1NDQzMTE5ODc3NjUzMzExOTk4NjY0NDMxMDA5Nzc2NTMzMjAwODg2NTU0MjExOTk=")

@timer
def decrypt_v4_B():
    for i in range(iterations):
        edV4_B.decrypt("MDk2NjA3NDMwMDc4NzExNTM4MTk2ODIyNjU4MzIwOTM5NzY5NDM0MDQwODg3NTMzMTU0OTcyNjQ0")

@timer
def decrypt_v4_C():
    for i in range(iterations):
        edV4_C.decrypt("dzN4TjN3eDBzbjN1bzB6ZTBleQ==")

@timer
def decrypt_v3():
    for i in range(iterations):
        edV3.decrypt("dzV1Ujh1ejh4aDRzcTR3aTd6eA==")

@timer
def decrypt_v2():
    for i in range(iterations):
        EncryptDecryptV2_0.decrypt("eDVkQjRkajF4czRoejZ0dzd1aA==")

@timer 
def decrypt_v1():
    for i in range(iterations):
        EncryptDecryptV1_0.decrypt("ZnhEdGlhdnhhdHR0bQ==")



@timer
def encrypt_v5():
    for i in range(iterations):
        edV_5.encrypt("This is a longer message to test the speed of methods when handling longer messages")

@timer
def encrypt_v4_A():
    for i in range(iterations):
        edV4_A.encrypt("This is a longer message to test the speed of methods when handling longer messages")

@timer
def encrypt_v4_B():
    for i in range(iterations):
        edV4_B.encrypt("This is a longer message to test the speed of methods when handling longer messages")

@timer
def encrypt_v4_C():
    for i in range(iterations):
        edV4_C.encrypt("This is a longer message to test the speed of methods when handling longer messages")

@timer
def encrypt_v3():
    for i in range(iterations):
        edV3.encrypt("This is a longer message to test the speed of methods when handling longer messages")

@timer
def encrypt_v2():
    for i in range(iterations):
        EncryptDecryptV2_0.encrypt("This is a longer message to test the speed of methods when handling longer messages")

@timer 
def encrypt_v1():
    for i in range(iterations):
        EncryptDecryptV1_0.encrypt("This is a longer message to test the speed of methods when handling longer messages")

decrypt_v5()
decrypt_v4_A()
decrypt_v4_B()
decrypt_v4_C()
decrypt_v3()
decrypt_v2()
decrypt_v1()

encrypt_v5()
encrypt_v4_A()
encrypt_v4_B()
encrypt_v4_C()
encrypt_v3()
encrypt_v2()
encrypt_v1()
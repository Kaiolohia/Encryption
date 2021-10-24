import EncryptDecryptV5_0
import EncryptDecryptV4_A
import EncryptDecryptV4_B
import EncryptDecryptV4_C
import time
iterations = 10000
edV_5 = EncryptDecryptV5_0.EncryptDecrypt()
edV4_A = EncryptDecryptV4_A.EncryptDecrypt()
edV4_B = EncryptDecryptV4_B.EncryptDecrypt()
edV4_C = EncryptDecryptV4_C.EncryptDecrypt()

#all of the decrypt tasks are each versions output of "Sample"

start_V5 = time.time()
for i in range(iterations):
    print(i)
    edV_5.decrypt("lPxyBPxFqS9QQKqZJeIORXELXVqyqD")
V5_time = time.time() - start_V5

start_V4A = time.time()
for i in range(iterations):
    print(i)
    edV4_A.decrypt("OTk4NzU1NDMxMDA5Nzc1NTMzMjE5OTg3NTUzMzEwOTg3NjY1NDIxMDk5ODc1NTMyMTEwOTg2NTUzMjIxMDg3NjU1NDMxMTk5Nzc2NDQzMTA5ODg3NTUzMjExMDk4NjY0MzMyMDA4Nzc1NDQzMTE5ODc3NjUzMzExOTk4NjY0NDMxMDA5Nzc2NTMzMjAwODg2NTU0MjExOTk=")
V4A_time = time.time() - start_V4A

start_V4B = time.time()
for i in range(iterations):
    print(i)
    edV4_B.decrypt("MDk2NjA3NDMwMDc4NzExNTM4MTk2ODIyNjU4MzIwOTM5NzY5NDM0MDQwODg3NTMzMTU0OTcyNjQ0")
V4B_time = time.time() - start_V4B


start_V4C = time.time()
for i in range(iterations):
    print(i)
    edV4_C.decrypt("dzN4TjN3eDBzbjN1bzB6ZTBleQ==")
V4C_time = time.time() - start_V4C

print(f"Total time for {iterations} iterations using V5 is {V5_time}")
print(f"Total time for {iterations} iterations using V4_A is {V4A_time}")
print(f"Total time for {iterations} iterations using V4_B is {V4B_time}")
print(f"Total time for {iterations} iterations using V4_C is {V4C_time}")
iterations = 1000
start_V5 = time.time()
for i in range(iterations):
    edV_5.encrypt("This is a longer message to test the speed of methods when handling longer messages")
V5_time = time.time() - start_V5
start_V4A = time.time()
for i in range(iterations):
    edV4_A.encrypt("This is a longer message to test the speed of methods when handling longer messages")
V4A_time = time.time() - start_V4A

start_V4B = time.time()
for i in range(iterations):
    edV4_B.encrypt("This is a longer message to test the speed of methods when handling longer messages")
V4B_time = time.time() - start_V4B

start_V4C = time.time()
for i in range(iterations):
    edV4_C.encrypt("This is a longer message to test the speed of methods when handling longer messages")
V4C_time = time.time() - start_V4C

print(f"\nTotal time for {iterations} iterations using V5 is {V5_time}")
print(f"Total time for {iterations} iterations using V4_A is {V4A_time}")
print(f"Total time for {iterations} iterations using V4_B is {V4B_time}")
print(f"Total time for {iterations} iterations using V4_C is {V4C_time}")
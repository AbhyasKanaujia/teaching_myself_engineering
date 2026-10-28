import os
import time

p = [0]
print(f"({os.getpid()}) memory address of p: {hex(id(p))}")

while True:
    time.sleep(1)
    p[0] += 1
    print(f"({os.getpid()}) p: {p[0]}")

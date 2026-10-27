import sys
import time


def spin(seconds):
    start = time.time()
    while time.time() - start < seconds:
        pass


word = sys.argv[1]
while True:
    spin(1)
    print(word, flush=True)

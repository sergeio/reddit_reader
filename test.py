import time
import sys

for x in range(10):
    sys.stdout.write('\r{0}\n3'.format(x))
    sys.stdout.flush()
    time.sleep(.5)
print

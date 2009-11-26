import random
import math

def roll(n, s):
    "Roll nDs's"
    if n==1:
        return random.randint(1,s)
    return sum(random.randint(1,s) for x in xrange(n))

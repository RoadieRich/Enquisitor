import random
import math
import sys


def roll(n, s):
    "Roll nDs's"
    if n==1:
        return random.randint(1,s)
    return sum(random.randint(1,s) for x in xrange(n))

def null(object):
    def __cmp__(self, other):
        return False
    def __bool__(self):
        return False

def round(n):
    return int(math.round(n))

class _Crit(object):
    """Unique object used to indicate critical success on stat tests"""
    #XXX: Use singleton pattern?
    def __repr__(self):
        return "Critical Success"
    def __bool__(self):
        return True

crit = _Crit()


#set to true to enable debugging output to stdout
DEBUG = False

#function used to output debugging information
debugOut = sys.stdout.write

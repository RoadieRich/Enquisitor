##  Enquisitor, a digital Inquisitor Games Master    
##  Copyright (C) 2009  Rich Lovely
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.



import random
import math
import sys


def roll(n, s, individuals=False, debug=False):
    "Roll nDs's.  Pass individuals=True to get a list of individual rolls"
    rolls = [random.randint(1,s) for x in xrange(n)]
    if debug or DEBUG:
        debugOut("Rolls: %s\n" % rolls)

    if individuals:
        return rolls
    else:
        tot = sum(rolls)
        if debug or DEBUG: debugOut("Total roll: %s\n" % tot)
        return tot

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

class _epicFail(object):
    """Unique object used to indicate critical failure on stat tests"""
    #XXX: Use singleton pattern?
    def __repr__(self):
        return "Critical Failure"
    def __bool__(self):
        return False

epicFail = _epicFail()

#set to true to enable debugging output to stdout
DEBUG = False

#function used to output debugging information
debugOut = sys.stdout.write

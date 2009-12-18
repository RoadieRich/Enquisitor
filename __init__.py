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



import util, characters


import sys as _sys


def test(stat, debug=False):
    """Take a test against a percentage stat. Pass debug=True to ouput
    roll details to stdout."""

    r = util.roll(1,100)
    if debug or util.DEBUG:
        util.debugOut("roll: %d, stat: %d\n"%(r,stat))
    result = False
    if stat > 5:
        if r <= round(stat/10.):
            result = util.crit
        elif r <= stat:
            result = True
    elif r <= 5:
        result = True    
    if debug or util.DEBUG:
        util.debugOut("result: %r\n" % result)
    return result

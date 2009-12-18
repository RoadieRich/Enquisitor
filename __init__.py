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

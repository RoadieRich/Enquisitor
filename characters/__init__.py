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



import math

from enquisitor.util import *

def _round(n):
    return int(round(n))

__all__ = ["Character"]

class Character(object):
    def __init__(self, **kwargs):
        if "archetype" in kwargs:
            kwargs["archetype"].generate(self)
        else:
            for stat, defval in {"T":0, "I":0, "WP":0, "Sg":0, "Nv":0, "Ld":0, "abilities":[], "equipment":[]}.iteritems(): 
                setattr(self, stat, kwargs.get(stat, defval))
        self.speedMods = 0
        self.movementMods = []
        self.injuryTotal = 0
        WS, BS, S = kwargs.get("WS", 0), kwargs.get("BS", 0), kwargs.get("S", 0)
        self.weaponSkill = {"left": (WS/2.), "right": (WS/2.)}
        self.WS = perSide(self.weaponSkill)
        self.balisticSkill = {"left": (BS/2.), "right": (BS/2.)}
        self.BS = perSide(self.balisticSkill)
        self.strength = {"left": (S/2.), "right": (S/2.)}
        self.S = perSide(self.strength)
        
        self.locations = HumanoidLocations(self)

    @property
    def systemShockValue(self):
        return math.ceil(self.T/5.)

    @property
    def knockbackValue(self):
        return math.ceil(self.S/10.)

    @property
    def baseInjuryValue(self):
        return math.ceil(self.T/10)

    @property
    def speed(self):
        return 1 + math.ceil(self.I/20.) + self.speedMods

    @speed.setter
    def speed(self,value):
        self.speedMods = value - self.speed

class perSide(object):
    def __init__(self, vals):
        self.vals = vals
    def __call__(self):
        return _round(sum(self.vals.itervalues()))
    def __getitem__(self, index):
        return _round(self.vals[index])
    def __repr__(self):
        return str(self())
    def __add__(self, val):
        return self() + val
    __radd__ = __add__
    def __mul__(self, val):
        return self() * val
    __rmul__ = __mul__
    def __div__(self, val):
        return self() / val
    def __rdiv__(self, val):
        return val/self()
    def __sub__(self, val):
        return self() - val
    def __rsub__(self, val):
        return val - self()
    def __cmp__(self, val):
        return cmp(self(), val)
    def __int__(self):
        return self()
class Locations(object):
    def __init__(self,character):
        self.character = character    
    def getLocation(self):
        r = roll(1, 100)
        for val, loc in self.locations:
            if r <= val:
                return loc

class HumanoidLocations(Locations):
    def __init__(self, character):
        super(HumanoidLocations, self).__init__(character)
        self.locations = ((96, Head(character)),
                          (81, Chest(character)),
                          (66, Abdomen(character)),
                          (51, Arm(character, "left")),
                          (36, Arm(character, "right")),
                          (31, Groin(character)),
                          (16, Leg(character, "left")),
                          (1, Leg(character, "right")))

class Location(object):
    def __init__(self, character):
        self.character = character
        self.armour = 0
        self.nextInjury = self.doLight
        self.bleeding = False

    def doLight(self):
        self.lightEffect()
        self.nextInjury = self.doHeavy

    def doHeavy(self):
        self.heavyEffect()
        self.nextInjury = self.doSerious

    def doSerious(self):
        self.seriousEffect()
        self.nextInjury = self.doAcute

    def doAcute(self):
        self.acuteEffect()
        self.nextInjury = self.doCrippled

    def doCrippled(self):
        self.crippledEffect()
        self.nextInjury = None

    def injure(self):
        if self.nextInjury:
            self.nextInjury()

    def hit(self, weapon):
        if hasattr(weapon, special):
            weapon.doHit(self)
        else:
            damage = weapon.getDamage()
            if damage >= self.character.knockbackValue:
                self.character.doKnockback()
            damage -= armour
            if damage >= self.character.systemShockValue:
                self.character.testSystemShock()
            levels = math.ceil(float(damage) / self.character.baseInjuryValue)
            for c in xrange(levels):
                self.injure()
            
class Head(Location):
    def lightEffecct(self):
        self.character.doStunned(roll(1,3))

    def doHeavy(self):
        self.heavyEffect()
        self.nextInjury = self.doAcute

    def heavyEffect(self):
        self.lightEffect()
        self.character.injuryTotal += roll(1,6)
        self.character.speed -= 1

    def acuteEffect(self):
        self.character.doSystemShock()

    def crippledEffect(self):
        self.character.doDead()
        
class Chest(Location):
    def lightEffecct(self):
        self.character.doProne()

    def heavyEffect(self):
        self.lightEffect()
        self.character.speed -= 1

    def seriousEffect(self):
        self.heavyEffect()
        character.doStunned(roll(1,6))
        character.injuryTotal += roll(1,3)

    def acuteEffect(self):
        self.heavyEffect()
        self.bleeding = True

    def crippledEffect(self):
        self.character.doSystemShock()

class Abdomen(Location):
    def lightEffecct(self):
        self.character.injuryTotal += roll(1,3)

    def heavyEffect(self):
        self.lightEffect()
        self.character.doProne()
        self.character.speed -= 1

    def seriousEffect(self):
        self.heavyEffect()
        self.bleeding = True

    def acuteEffect(self):
        self.seriousEffect()
        self.character.doStunned(roll(1,3))

    def crippledEffect(self):
        self.acuteEffect()
        self.character.maxSpeed = "Crawl"

class Groin(Location):
    def lightEffecct(self):
        self.character.doProne()

    def doHeavy(self):
        self.heavyEffect()
        self.nextInjury = self.doAcute

    def heavyEffect(self):
        self.lightEffect()
        self.character.doStunned(roll(1,3))
        self.character.speed -= 1

    def acuteEffect(self):
        self.heavyEffect()
        self.character.injuryTotal += roll(1,3)
        self.bleeding = True

    def crippledEffect(self):
        self.character.doSystemShock()

class Limb(Location):
    def __init__(self, character, side):
        super(Limb, self).__init__(character)
        self.side = side

    def lightEffecct(self):
        "'tis Nothing!"

class Arm(Limb):
    def heavyEffect(self):
        if not self.character.testStrength(self.side):
            self.character.drop(self.side)

    def seriousEffect(self):
        self.heavyEffect()
        self.character.strength[self.side] = math.ceil(self.character.strength[self.side]/2.)
        self.character.weaponSkill[self.side] = math.ceil(self.character.weaponSkill[self.side]/2.)
        self.character.balisticSkill[self.side] = math.ceil(self.character.balisticSkill[self.side]/2.)
        self.character.injuryTotal += roll(1,3)

    def acuteEffect(self):
        self.character.drop(self.side)
        self.character.strength[self.side] = null()
        self.character.weaponSkill[self.side] = null()
        self.character.balisticSkill[self.side] = null()
        self.bleeding = True

    def crippledEffect(self):
        self.character.testSystemShock()
        self.acuteEffect()

class Leg(Limb):
    def heavyEffect(self):
        self.character.speed -= 1

    def seriousEffect(self):
        self.heavyEffect()
        self.character.injuryTotal += roll(1,3)
        self.character.movementMods.append("*0.5")
        
    def acuteEffect(self):
        self.seriousEffect()
        self.maxSpeed = "crawl"
        self.bleeding = True

    def crippledEffect(self):
        self.acuteEffect()
        self.character.testSystemShock()


        
        

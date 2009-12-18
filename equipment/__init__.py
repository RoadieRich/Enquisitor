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



import ranged, melee, special

__all__ = ["ranged", "melee", "special"]


class Base(object):
    def __init__(self):
        self.weight = 0
        self.rarity = 0
        self.specialRules = []

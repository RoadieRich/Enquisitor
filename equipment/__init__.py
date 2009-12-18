import ranged, melee, special

__all__ = ["ranged", "melee", "special"]


class Base(object):
    def __init__(self):
        self.weight = 0
        self.rarity = 0
        self.specialRules = []

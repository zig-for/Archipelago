from .itemInfo import ItemInfo
from .constants import *


class TunicFairy(ItemInfo):

    def __init__(self, index):
        self.index = index
        super().__init__(0x301)
        
    def patch(self, rom, option, *, multiworld=None):
        assert multiworld is None
        rom.banks[0x36][0x11BF + self.index] = CHEST_ITEMS[option]

    def read(self, rom):
        value = rom.banks[0x36][0x11BF + self.index]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find tunic fairy contents in ROM (0x%02x)" % (value))

    @property
    def nameId(self):
        return "0x%03X-%s" % (self.room, self.index)

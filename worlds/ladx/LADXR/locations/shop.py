from .itemInfo import ItemInfo
from .constants import *
from ..utils import formatText
from ..assembler import ASM


class ShopItem(ItemInfo):
    def __init__(self, index):
        self.__index = index
        super().__init__(0x2A1)

    def patch(self, rom, option, *, multiworld=None):
        assert multiworld is None
        if self.__index == 0:
            rom.patch(0x04, 0x37C5, "08", "%02X" % (CHEST_ITEMS[option]))
            rom.texts[0x030] = formatText("Deluxe {%s} 200 {RUPEES}!" % (option), ask="Buy  No Way")
        elif self.__index == 1:
            rom.patch(0x04, 0x37C6, "02", "%02X" % (CHEST_ITEMS[option]))
            rom.texts[0x02C] = formatText("{%s} Only 980 {RUPEES}!" % (option), ask="Buy  No Way")

    def read(self, rom):
        value = rom.banks[0x04][0x37C5 + self.__index]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find shop item contents in ROM (0x%02x)" % (value))

    @property
    def nameId(self):
        return "0x%03X-%s" % (self.room, self.__index)

    def __repr__(self):
        return "%s(%d)" % (self.__class__.__name__, self.__index)

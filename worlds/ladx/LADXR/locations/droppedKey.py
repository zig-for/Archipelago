from .itemInfo import ItemInfo
from .constants import *
patched_already = {}

class DroppedKey(ItemInfo):
    OPTIONS = [POWER_BRACELET, SHIELD, BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, OCARINA,
        FEATHER, SHOVEL, MAGIC_POWDER, BOMB, SWORD, FLIPPERS, MAGNIFYING_LENS, MEDICINE,
        TAIL_KEY, ANGLER_KEY, FACE_KEY, BIRD_KEY, GOLD_LEAF, SLIME_KEY, ROOSTER,
        RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500,
        SEASHELL, BOOMERANG, HEART_PIECE, ARROWS_10, SINGLE_ARROW,
        MAX_POWDER_UPGRADE, MAX_BOMBS_UPGRADE, MAX_ARROWS_UPGRADE, RED_TUNIC, BLUE_TUNIC,
        HEART_CONTAINER, BAD_HEART_CONTAINER, TOADSTOOL, SONG1, SONG2, SONG3,
        INSTRUMENT1, INSTRUMENT2, INSTRUMENT3, INSTRUMENT4, INSTRUMENT5, INSTRUMENT6, INSTRUMENT7, INSTRUMENT8,
        TRADING_ITEM_YOSHI_DOLL, TRADING_ITEM_RIBBON, TRADING_ITEM_DOG_FOOD, TRADING_ITEM_BANANAS, TRADING_ITEM_STICK,
        TRADING_ITEM_HONEYCOMB, TRADING_ITEM_PINEAPPLE, TRADING_ITEM_HIBISCUS, TRADING_ITEM_LETTER, TRADING_ITEM_BROOM,
        TRADING_ITEM_FISHING_HOOK, TRADING_ITEM_NECKLACE, TRADING_ITEM_SCALE, TRADING_ITEM_MAGNIFYING_GLASS
    ]
    MULTIWORLD = True
    default_item = None

    def __init__(self, room=None):
        extra = None
        if room == 0x169:  # Room in D4 where the key drops down the hole into the sidescroller
            extra = 0x017C
        elif room == 0x166:  # D4 boss, also place the item in out real boss room.
            extra = 0x01ff
        elif room == 0x223:  # D7 boss, also place the item in our real boss room.
            extra = 0x02E8
        elif room == 0x092:  # Marins song
            extra = 0x00DC
        super().__init__(room, extra)
    def patch(self, rom, option, *, multiworld=None):
        if (option.startswith(MAP) and option != MAP) or (option.startswith(COMPASS) and option != COMPASS) or option.startswith(STONE_BEAK) or (option.startswith(NIGHTMARE_KEY) and option != NIGHTMARE_KEY )or (option.startswith(KEY) and option != KEY):
            if option[-1] == 'P':
                print(option)
            if self._location.dungeon == int(option[-1]) and multiworld is None and self.room not in {0x166, 0x223}:
                option = option[:-1]
        rom.banks[0x3E][self.room + 0x3800] = CHEST_ITEMS[option]
        #assert room not in patched_already, f"{self} {patched_already[room]}"
        #patched_already[room] = self


        if self.extra:
            assert(not self.default_item)
            rom.banks[0x3E][self.extra + 0x3800] = CHEST_ITEMS[option]

        if multiworld is not None:
            rom.banks[0x3E][0x3300 + self.room] = multiworld
            
            if self.extra:
                rom.banks[0x3E][0x3300 + self.extra] = multiworld

    def read(self, rom):
        assert self._location is not None, hex(self.room)
        value = rom.banks[0x3E][self.room + 0x3800]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                if k in [MAP, COMPASS, STONE_BEAK, NIGHTMARE_KEY, KEY]:
                    assert self._location.dungeon is not None, "Dungeon item outside of dungeon? %r" % (self)
                    return "%s%d" % (k, self._location.dungeon)
                return k
        raise ValueError("Could not find chest contents in ROM (0x%02x)" % (value))

    def __repr__(self):
        if self._location and self._location.dungeon:
            return "%s:%03x:%d" % (self.__class__.__name__, self.room, self._location.dungeon)
        else:
            return "%s:%03x" % (self.__class__.__name__, self.room)

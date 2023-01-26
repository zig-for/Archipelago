from .itemInfo import ItemInfo
from .constants import *
from .droppedKey import DroppedKey
from ..assembler import ASM
from ..utils import formatText
from ..roomEditor import RoomEditor


class StartItem(DroppedKey):
    # We need to give something here that we can use to progress.
    # FEATHER
    OPTIONS = [SWORD, SHIELD, POWER_BRACELET, OCARINA,  BOOMERANG, MAGIC_ROD, TAIL_KEY, SHOVEL, HOOKSHOT, PEGASUS_BOOTS, MAGIC_POWDER, BOMB]

    OPTIONS_ANY = [POWER_BRACELET, SHIELD, BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, OCARINA,
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
    MULTIWORLD = False

    def __init__(self):
        super().__init__(0x2A3)
        self.give_bowwow = False
        self.local_only = True

    def configure(self, options):
        if options.bowwow != 'normal':
            # When we have bowwow mode, we pretend to be a sword for logic reasons
            self.OPTIONS = [SWORD]
            self.give_bowwow = True
        if options.randomstartlocation and options.entranceshuffle != 'none':
            self.OPTIONS.append(FLIPPERS)

    def patch(self, rom, option, *, multiworld=None):
        assert multiworld is None

        if self.give_bowwow:
            option = BOWWOW
            rom.texts[0xC8] = formatText("Got BowWow!")

        if option != SHIELD:
            rom.patch(5, 0x0CDA, ASM("ld a, $22"), ASM("ld a, $00"))  # do not change links sprite into the one with a shield

        super().patch(rom, option)

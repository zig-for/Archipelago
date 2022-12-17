from BaseClasses import Item, ItemClassification
from . import Common
import typing
from enum import IntEnum
from .LADXR.locations.constants import CHEST_ITEMS


class ItemData(typing.NamedTuple):
    item_name: str
    ladxr_id: str
    progression: bool
    @property
    def item_id(self):
        return CHEST_ITEMS[self.ladxr_id]


class DungeonItemType(IntEnum):
    INSTRUMENT = 0
    NIGHTMARE_KEY = 1
    KEY = 2
    STONE_BEAK = 3
    MAP = 4
    COMPASS = 5

class DungeonItemData(ItemData):
    @property
    def dungeon_index(self):
        return int(self.ladxr_id[-1])
    
    @property
    def dungeon_item_type(self):
        s = self.ladxr_id[:-1]
        return DungeonItemType.__dict__[s]

class LinksAwakeningItem(Item):
    game: str = Common.LINKS_AWAKENING

    def __init__(self, item_data, player):
        classification = ItemClassification.progression if item_data.progression else ItemClassification.filler
        super().__init__(item_data.item_name, classification, Common.BASE_ID + item_data.item_id, player)
        self.item_data = item_data

# TODO: use _NAMES instead?
class ItemName:
    POWER_BRACELET = "Power Bracelet"
    SHIELD = "Shield"
    BOW = "Bow"
    HOOKSHOT = "Hookshot"
    MAGIC_ROD = "Magic Rod"
    PEGASUS_BOOTS = "Pegasus Boots"
    OCARINA = "Ocarina"
    FEATHER = "Feather"
    SHOVEL = "Shovel"
    MAGIC_POWDER = "Magic Powder"
    BOMB = "Bomb"
    SWORD = "Sword"
    FLIPPERS = "Flippers"
    MAGNIFYING_LENS = "Magnifying Lens"
    MEDICINE = "Medicine"
    TAIL_KEY = "Tail Key"
    ANGLER_KEY = "Angler Key"
    FACE_KEY = "Face Key"
    BIRD_KEY = "Bird Key"
    SLIME_KEY = "Slime Key"
    GOLD_LEAF = "Gold Leaf"
    RUPEES_50 = "20 Rupees"
    RUPEES_20 = "50 Rupees"
    RUPEES_100 = "100 Rupees"
    RUPEES_200 = "200 Rupees"
    RUPEES_500 = "500 Rupees"
    SEASHELL = "Seashell"
    MESSAGE = "Message"
    GEL = "Gel"
    BOOMERANG = "Boomerang"
    HEART_PIECE = "Heart Piece"
    BOWWOW = "Bowwow"
    ARROWS_10 = "Arrows 10"
    SINGLE_ARROW = "Single Arrow"
    ROOSTER = "Rooster"
    MAX_POWDER_UPGRADE = "Max Powder Upgrade"
    MAX_BOMBS_UPGRADE = "Max Bombs Upgrade"
    MAX_ARROWS_UPGRADE = "Max Arrows Upgrade"
    RED_TUNIC = "Red Tunic"
    BLUE_TUNIC = "Blue Tunic"
    HEART_CONTAINER = "Heart Container"
    BAD_HEART_CONTAINER = "Bad Heart Container"
    TOADSTOOL = "Toadstool"
    KEY = "Key"
    KEY1 = "Key1"
    KEY2 = "Key2"
    KEY3 = "Key3"
    KEY4 = "Key4"
    KEY5 = "Key5"
    KEY6 = "Key6"
    KEY7 = "Key7"
    KEY8 = "Key8"
    KEY9 = "Key9"
    NIGHTMARE_KEY = "Nightmare Key"
    NIGHTMARE_KEY1 = "Nightmare Key1"
    NIGHTMARE_KEY2 = "Nightmare Key2"
    NIGHTMARE_KEY3 = "Nightmare Key3"
    NIGHTMARE_KEY4 = "Nightmare Key4"
    NIGHTMARE_KEY5 = "Nightmare Key5"
    NIGHTMARE_KEY6 = "Nightmare Key6"
    NIGHTMARE_KEY7 = "Nightmare Key7"
    NIGHTMARE_KEY8 = "Nightmare Key8"
    NIGHTMARE_KEY9 = "Nightmare Key9"
    MAP = "Map"
    MAP1 = "Map1"
    MAP2 = "Map2"
    MAP3 = "Map3"
    MAP4 = "Map4"
    MAP5 = "Map5"
    MAP6 = "Map6"
    MAP7 = "Map7"
    MAP8 = "Map8"
    MAP9 = "Map9"
    COMPASS = "Compass"
    COMPASS1 = "Compass1"
    COMPASS2 = "Compass2"
    COMPASS3 = "Compass3"
    COMPASS4 = "Compass4"
    COMPASS5 = "Compass5"
    COMPASS6 = "Compass6"
    COMPASS7 = "Compass7"
    COMPASS8 = "Compass8"
    COMPASS9 = "Compass9"
    STONE_BEAK = "Stone Beak"
    STONE_BEAK1 = "Stone Beak1"
    STONE_BEAK2 = "Stone Beak2"
    STONE_BEAK3 = "Stone Beak3"
    STONE_BEAK4 = "Stone Beak4"
    STONE_BEAK5 = "Stone Beak5"
    STONE_BEAK6 = "Stone Beak6"
    STONE_BEAK7 = "Stone Beak7"
    STONE_BEAK8 = "Stone Beak8"
    STONE_BEAK9 = "Stone Beak9"
    SONG1 = "Song1"
    SONG2 = "Song2"
    SONG3 = "Song3"
    INSTRUMENT1 = "Instrument1"
    INSTRUMENT2 = "Instrument2"
    INSTRUMENT3 = "Instrument3"
    INSTRUMENT4 = "Instrument4"
    INSTRUMENT5 = "Instrument5"
    INSTRUMENT6 = "Instrument6"
    INSTRUMENT7 = "Instrument7"
    INSTRUMENT8 = "Instrument8"
    TRADING_ITEM_YOSHI_DOLL = "Trading Item Yoshi Doll"
    TRADING_ITEM_RIBBON = "Trading Item Ribbon"
    TRADING_ITEM_DOG_FOOD = "Trading Item Dog Food"
    TRADING_ITEM_BANANAS = "Trading Item Bananas"
    TRADING_ITEM_STICK = "Trading Item Stick"
    TRADING_ITEM_HONEYCOMB = "Trading Item Honeycomb"
    TRADING_ITEM_PINEAPPLE = "Trading Item Pineapple"
    TRADING_ITEM_HIBISCUS = "Trading Item Hibiscus"
    TRADING_ITEM_LETTER = "Trading Item Letter"
    TRADING_ITEM_BROOM = "Trading Item Broom"
    TRADING_ITEM_FISHING_HOOK = "Trading Item Fishing Hook"
    TRADING_ITEM_NECKLACE = "Trading Item Necklace"
    TRADING_ITEM_SCALE = "Trading Item Scale"
    TRADING_ITEM_MAGNIFYING_GLASS = "Trading Item Magnifying Glass"


links_awakening_items = [
    ItemData(ItemName.POWER_BRACELET, "POWER_BRACELET", True),
    ItemData(ItemName.SHIELD, "SHIELD", True),
    ItemData(ItemName.BOW, "BOW", True),
    ItemData(ItemName.HOOKSHOT, "HOOKSHOT", True),
    ItemData(ItemName.MAGIC_ROD, "MAGIC_ROD", True),
    ItemData(ItemName.PEGASUS_BOOTS, "PEGASUS_BOOTS", True),
    ItemData(ItemName.OCARINA, "OCARINA", True),
    ItemData(ItemName.FEATHER, "FEATHER", True),
    ItemData(ItemName.SHOVEL, "SHOVEL", True),
    ItemData(ItemName.MAGIC_POWDER, "MAGIC_POWDER", True),
    ItemData(ItemName.BOMB, "BOMB", True),
    ItemData(ItemName.SWORD, "SWORD", True),
    ItemData(ItemName.FLIPPERS, "FLIPPERS", True),
    ItemData(ItemName.MAGNIFYING_LENS, "MAGNIFYING_LENS", True),
    ItemData(ItemName.MEDICINE, "MEDICINE", True),
    ItemData(ItemName.TAIL_KEY, "TAIL_KEY", True),
    ItemData(ItemName.ANGLER_KEY, "ANGLER_KEY", True),
    ItemData(ItemName.FACE_KEY, "FACE_KEY", True),
    ItemData(ItemName.BIRD_KEY, "BIRD_KEY", True),
    ItemData(ItemName.SLIME_KEY, "SLIME_KEY", True),
    ItemData(ItemName.GOLD_LEAF, "GOLD_LEAF", True),
    ItemData(ItemName.RUPEES_50, "RUPEES_50", True),
    ItemData(ItemName.RUPEES_20, "RUPEES_20", True),
    ItemData(ItemName.RUPEES_100, "RUPEES_100", True),
    ItemData(ItemName.RUPEES_200, "RUPEES_200", True),
    ItemData(ItemName.RUPEES_500, "RUPEES_500", True),
    ItemData(ItemName.SEASHELL, "SEASHELL", True),
    ItemData(ItemName.MESSAGE, "MESSAGE", True),
    ItemData(ItemName.GEL, "GEL", True),
    ItemData(ItemName.BOOMERANG, "BOOMERANG", True),
    ItemData(ItemName.HEART_PIECE, "HEART_PIECE", True),
    ItemData(ItemName.BOWWOW, "BOWWOW", True),
    ItemData(ItemName.ARROWS_10, "ARROWS_10", True),
    ItemData(ItemName.SINGLE_ARROW, "SINGLE_ARROW", False),
    ItemData(ItemName.ROOSTER, "ROOSTER", True),
    ItemData(ItemName.MAX_POWDER_UPGRADE, "MAX_POWDER_UPGRADE", False),
    ItemData(ItemName.MAX_BOMBS_UPGRADE, "MAX_BOMBS_UPGRADE", False),
    ItemData(ItemName.MAX_ARROWS_UPGRADE, "MAX_ARROWS_UPGRADE", False),
    ItemData(ItemName.RED_TUNIC, "RED_TUNIC", True),
    ItemData(ItemName.BLUE_TUNIC, "BLUE_TUNIC", True),
    ItemData(ItemName.HEART_CONTAINER, "HEART_CONTAINER", True),
    #ItemData(ItemName.BAD_HEART_CONTAINER, "BAD_HEART_CONTAINER", True),
    ItemData(ItemName.TOADSTOOL, "TOADSTOOL", True),
    #DungeonItemData(ItemName.KEY, "KEY", True),
    DungeonItemData(ItemName.KEY1, "KEY1", True),
    DungeonItemData(ItemName.KEY2, "KEY2", True),
    DungeonItemData(ItemName.KEY3, "KEY3", True),
    DungeonItemData(ItemName.KEY4, "KEY4", True),
    DungeonItemData(ItemName.KEY5, "KEY5", True),
    DungeonItemData(ItemName.KEY6, "KEY6", True),
    DungeonItemData(ItemName.KEY7, "KEY7", True),
    DungeonItemData(ItemName.KEY8, "KEY8", True),
    DungeonItemData(ItemName.KEY9, "KEY9", True),
    DungeonItemData(ItemName.NIGHTMARE_KEY, "NIGHTMARE_KEY", True),
    DungeonItemData(ItemName.NIGHTMARE_KEY1, "NIGHTMARE_KEY1", True),
    DungeonItemData(ItemName.NIGHTMARE_KEY2, "NIGHTMARE_KEY2", True),
    DungeonItemData(ItemName.NIGHTMARE_KEY3, "NIGHTMARE_KEY3", True),
    DungeonItemData(ItemName.NIGHTMARE_KEY4, "NIGHTMARE_KEY4", True),
    DungeonItemData(ItemName.NIGHTMARE_KEY5, "NIGHTMARE_KEY5", True),
    DungeonItemData(ItemName.NIGHTMARE_KEY6, "NIGHTMARE_KEY6", True),
    DungeonItemData(ItemName.NIGHTMARE_KEY7, "NIGHTMARE_KEY7", True),
    DungeonItemData(ItemName.NIGHTMARE_KEY8, "NIGHTMARE_KEY8", True),
    DungeonItemData(ItemName.NIGHTMARE_KEY9, "NIGHTMARE_KEY9", True),
    #DungeonItemData(ItemName.MAP, "MAP", False),
    DungeonItemData(ItemName.MAP1, "MAP1", False),
    DungeonItemData(ItemName.MAP2, "MAP2", False),
    DungeonItemData(ItemName.MAP3, "MAP3", False),
    DungeonItemData(ItemName.MAP4, "MAP4", False),
    DungeonItemData(ItemName.MAP5, "MAP5", False),
    DungeonItemData(ItemName.MAP6, "MAP6", False),
    DungeonItemData(ItemName.MAP7, "MAP7", False),
    DungeonItemData(ItemName.MAP8, "MAP8", False),
    DungeonItemData(ItemName.MAP9, "MAP9", False),
    #DungeonItemData(ItemName.COMPASS, "COMPASS", False),
    DungeonItemData(ItemName.COMPASS1, "COMPASS1", False),
    DungeonItemData(ItemName.COMPASS2, "COMPASS2", False),
    DungeonItemData(ItemName.COMPASS3, "COMPASS3", False),
    DungeonItemData(ItemName.COMPASS4, "COMPASS4", False),
    DungeonItemData(ItemName.COMPASS5, "COMPASS5", False),
    DungeonItemData(ItemName.COMPASS6, "COMPASS6", False),
    DungeonItemData(ItemName.COMPASS7, "COMPASS7", False),
    DungeonItemData(ItemName.COMPASS8, "COMPASS8", False),
    DungeonItemData(ItemName.COMPASS9, "COMPASS9", False),
    #DungeonItemData(ItemName.STONE_BEAK, "STONE_BEAK", False),
    DungeonItemData(ItemName.STONE_BEAK1, "STONE_BEAK1", False),
    DungeonItemData(ItemName.STONE_BEAK2, "STONE_BEAK2", False),
    DungeonItemData(ItemName.STONE_BEAK3, "STONE_BEAK3", False),
    DungeonItemData(ItemName.STONE_BEAK4, "STONE_BEAK4", False),
    DungeonItemData(ItemName.STONE_BEAK5, "STONE_BEAK5", False),
    DungeonItemData(ItemName.STONE_BEAK6, "STONE_BEAK6", False),
    DungeonItemData(ItemName.STONE_BEAK7, "STONE_BEAK7", False),
    DungeonItemData(ItemName.STONE_BEAK8, "STONE_BEAK8", False),
    DungeonItemData(ItemName.STONE_BEAK9, "STONE_BEAK9", False),
    ItemData(ItemName.SONG1, "SONG1", True),
    ItemData(ItemName.SONG2, "SONG2", True),  # TODO
    ItemData(ItemName.SONG3, "SONG3", True),  # TODO
    DungeonItemData(ItemName.INSTRUMENT1, "INSTRUMENT1", True),
    DungeonItemData(ItemName.INSTRUMENT2, "INSTRUMENT2", True),
    DungeonItemData(ItemName.INSTRUMENT3, "INSTRUMENT3", True),
    DungeonItemData(ItemName.INSTRUMENT4, "INSTRUMENT4", True),
    DungeonItemData(ItemName.INSTRUMENT5, "INSTRUMENT5", True),
    DungeonItemData(ItemName.INSTRUMENT6, "INSTRUMENT6", True),
    DungeonItemData(ItemName.INSTRUMENT7, "INSTRUMENT7", True),
    DungeonItemData(ItemName.INSTRUMENT8, "INSTRUMENT8", True),
    ItemData(ItemName.TRADING_ITEM_YOSHI_DOLL, "TRADING_ITEM_YOSHI_DOLL", True),
    ItemData(ItemName.TRADING_ITEM_RIBBON, "TRADING_ITEM_RIBBON", True),
    ItemData(ItemName.TRADING_ITEM_DOG_FOOD, "TRADING_ITEM_DOG_FOOD", True),
    ItemData(ItemName.TRADING_ITEM_BANANAS, "TRADING_ITEM_BANANAS", True),
    ItemData(ItemName.TRADING_ITEM_STICK, "TRADING_ITEM_STICK", True),
    ItemData(ItemName.TRADING_ITEM_HONEYCOMB, "TRADING_ITEM_HONEYCOMB", True),
    ItemData(ItemName.TRADING_ITEM_PINEAPPLE, "TRADING_ITEM_PINEAPPLE", True),
    ItemData(ItemName.TRADING_ITEM_HIBISCUS, "TRADING_ITEM_HIBISCUS", True),
    ItemData(ItemName.TRADING_ITEM_LETTER, "TRADING_ITEM_LETTER", True),
    ItemData(ItemName.TRADING_ITEM_BROOM, "TRADING_ITEM_BROOM", True),
    ItemData(ItemName.TRADING_ITEM_FISHING_HOOK, "TRADING_ITEM_FISHING_HOOK", True),
    ItemData(ItemName.TRADING_ITEM_NECKLACE, "TRADING_ITEM_NECKLACE", True),
    ItemData(ItemName.TRADING_ITEM_SCALE, "TRADING_ITEM_SCALE", True),
    ItemData(ItemName.TRADING_ITEM_MAGNIFYING_GLASS, "TRADING_ITEM_MAGNIFYING_GLASS", True)
]

ladxr_item_to_la_item_name = {
    item.ladxr_id: item.item_name for item in links_awakening_items
}

links_awakening_items_by_name = {
        item.item_name : item for item in links_awakening_items
    }

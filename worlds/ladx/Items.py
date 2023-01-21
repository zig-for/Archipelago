from BaseClasses import Item, ItemClassification
from . import Common
import typing
from enum import IntEnum
from .LADXR.locations.constants import CHEST_ITEMS


class ItemData(typing.NamedTuple):
    item_name: str
    ladxr_id: str
    classification: ItemClassification
    mark_only_first_progression: bool = False
    created_for_players = set()
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
        classfication = item_data.classification
        if item_data.mark_only_first_progression:
            if player in item_data.created_for_players:
                classfication = ItemClassification.filler
            else:
                item_data.created_for_players.add(player)
        super().__init__(item_data.item_name, item_data.classification, Common.BASE_ID + item_data.item_id, player)
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
    SWORD = "Progressive Sword"
    FLIPPERS = "Flippers"
    MAGNIFYING_LENS = "Magnifying Lens"
    MEDICINE = "Medicine"
    TAIL_KEY = "Tail Key"
    ANGLER_KEY = "Angler Key"
    FACE_KEY = "Face Key"
    BIRD_KEY = "Bird Key"
    SLIME_KEY = "Slime Key"
    GOLD_LEAF = "Gold Leaf"
    RUPEES_20 = "20 Rupees"
    RUPEES_50 = "50 Rupees"
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
    ItemData(ItemName.POWER_BRACELET, "POWER_BRACELET", ItemClassification.progression),
    ItemData(ItemName.SHIELD, "SHIELD", ItemClassification.progression),
    ItemData(ItemName.BOW, "BOW", ItemClassification.progression),
    ItemData(ItemName.HOOKSHOT, "HOOKSHOT", ItemClassification.progression),
    ItemData(ItemName.MAGIC_ROD, "MAGIC_ROD", ItemClassification.progression),
    ItemData(ItemName.PEGASUS_BOOTS, "PEGASUS_BOOTS", ItemClassification.progression),
    ItemData(ItemName.OCARINA, "OCARINA", ItemClassification.progression),
    ItemData(ItemName.FEATHER, "FEATHER", ItemClassification.progression),
    ItemData(ItemName.SHOVEL, "SHOVEL", ItemClassification.progression),
    ItemData(ItemName.MAGIC_POWDER, "MAGIC_POWDER", ItemClassification.progression, True),
    ItemData(ItemName.BOMB, "BOMB", ItemClassification.progression, True),
    ItemData(ItemName.SWORD, "SWORD", ItemClassification.progression),
    ItemData(ItemName.FLIPPERS, "FLIPPERS", ItemClassification.progression),
    ItemData(ItemName.MAGNIFYING_LENS, "MAGNIFYING_LENS", ItemClassification.progression),
    ItemData(ItemName.MEDICINE, "MEDICINE", ItemClassification.useful),
    ItemData(ItemName.TAIL_KEY, "TAIL_KEY", ItemClassification.progression),
    ItemData(ItemName.ANGLER_KEY, "ANGLER_KEY", ItemClassification.progression),
    ItemData(ItemName.FACE_KEY, "FACE_KEY", ItemClassification.progression),
    ItemData(ItemName.BIRD_KEY, "BIRD_KEY", ItemClassification.progression),
    ItemData(ItemName.SLIME_KEY, "SLIME_KEY", ItemClassification.progression),
    ItemData(ItemName.GOLD_LEAF, "GOLD_LEAF", ItemClassification.progression),
    ItemData(ItemName.RUPEES_20, "RUPEES_20", ItemClassification.filler),
    ItemData(ItemName.RUPEES_50, "RUPEES_50", ItemClassification.useful),
    ItemData(ItemName.RUPEES_100, "RUPEES_100", ItemClassification.progression_skip_balancing),
    ItemData(ItemName.RUPEES_200, "RUPEES_200", ItemClassification.progression_skip_balancing),
    ItemData(ItemName.RUPEES_500, "RUPEES_500", ItemClassification.progression_skip_balancing),
    ItemData(ItemName.SEASHELL, "SEASHELL", ItemClassification.progression_skip_balancing),
    ItemData(ItemName.MESSAGE, "MESSAGE", ItemClassification.progression),
    ItemData(ItemName.GEL, "GEL", ItemClassification.trap),
    ItemData(ItemName.BOOMERANG, "BOOMERANG", ItemClassification.progression),
    ItemData(ItemName.HEART_PIECE, "HEART_PIECE", ItemClassification.filler),
    ItemData(ItemName.BOWWOW, "BOWWOW", ItemClassification.progression),
    ItemData(ItemName.ARROWS_10, "ARROWS_10", ItemClassification.filler),
    ItemData(ItemName.SINGLE_ARROW, "SINGLE_ARROW", ItemClassification.filler),
    ItemData(ItemName.ROOSTER, "ROOSTER", ItemClassification.progression),
    ItemData(ItemName.MAX_POWDER_UPGRADE, "MAX_POWDER_UPGRADE", ItemClassification.filler),
    ItemData(ItemName.MAX_BOMBS_UPGRADE, "MAX_BOMBS_UPGRADE", ItemClassification.filler),
    ItemData(ItemName.MAX_ARROWS_UPGRADE, "MAX_ARROWS_UPGRADE", ItemClassification.filler),
    ItemData(ItemName.RED_TUNIC, "RED_TUNIC", ItemClassification.useful),
    ItemData(ItemName.BLUE_TUNIC, "BLUE_TUNIC", ItemClassification.useful),
    ItemData(ItemName.HEART_CONTAINER, "HEART_CONTAINER", ItemClassification.useful),
    #ItemData(ItemName.BAD_HEART_CONTAINER, "BAD_HEART_CONTAINER", ItemClassification.trap),
    ItemData(ItemName.TOADSTOOL, "TOADSTOOL", ItemClassification.progression),
    #DungeonItemData(ItemName.KEY, "KEY", ItemClassification.progression),
    DungeonItemData(ItemName.KEY1, "KEY1", ItemClassification.progression),
    DungeonItemData(ItemName.KEY2, "KEY2", ItemClassification.progression),
    DungeonItemData(ItemName.KEY3, "KEY3", ItemClassification.progression),
    DungeonItemData(ItemName.KEY4, "KEY4", ItemClassification.progression),
    DungeonItemData(ItemName.KEY5, "KEY5", ItemClassification.progression),
    DungeonItemData(ItemName.KEY6, "KEY6", ItemClassification.progression),
    DungeonItemData(ItemName.KEY7, "KEY7", ItemClassification.progression),
    DungeonItemData(ItemName.KEY8, "KEY8", ItemClassification.progression),
    DungeonItemData(ItemName.KEY9, "KEY9", ItemClassification.progression),
    DungeonItemData(ItemName.NIGHTMARE_KEY, "NIGHTMARE_KEY", ItemClassification.progression),
    DungeonItemData(ItemName.NIGHTMARE_KEY1, "NIGHTMARE_KEY1", ItemClassification.progression),
    DungeonItemData(ItemName.NIGHTMARE_KEY2, "NIGHTMARE_KEY2", ItemClassification.progression),
    DungeonItemData(ItemName.NIGHTMARE_KEY3, "NIGHTMARE_KEY3", ItemClassification.progression),
    DungeonItemData(ItemName.NIGHTMARE_KEY4, "NIGHTMARE_KEY4", ItemClassification.progression),
    DungeonItemData(ItemName.NIGHTMARE_KEY5, "NIGHTMARE_KEY5", ItemClassification.progression),
    DungeonItemData(ItemName.NIGHTMARE_KEY6, "NIGHTMARE_KEY6", ItemClassification.progression),
    DungeonItemData(ItemName.NIGHTMARE_KEY7, "NIGHTMARE_KEY7", ItemClassification.progression),
    DungeonItemData(ItemName.NIGHTMARE_KEY8, "NIGHTMARE_KEY8", ItemClassification.progression),
    DungeonItemData(ItemName.NIGHTMARE_KEY9, "NIGHTMARE_KEY9", ItemClassification.progression),
    #DungeonItemData(ItemName.MAP, "MAP", ItemClassification.filler),
    DungeonItemData(ItemName.MAP1, "MAP1", ItemClassification.filler),
    DungeonItemData(ItemName.MAP2, "MAP2", ItemClassification.filler),
    DungeonItemData(ItemName.MAP3, "MAP3", ItemClassification.filler),
    DungeonItemData(ItemName.MAP4, "MAP4", ItemClassification.filler),
    DungeonItemData(ItemName.MAP5, "MAP5", ItemClassification.filler),
    DungeonItemData(ItemName.MAP6, "MAP6", ItemClassification.filler),
    DungeonItemData(ItemName.MAP7, "MAP7", ItemClassification.filler),
    DungeonItemData(ItemName.MAP8, "MAP8", ItemClassification.filler),
    DungeonItemData(ItemName.MAP9, "MAP9", ItemClassification.filler),
    #DungeonItemData(ItemName.COMPASS, "COMPASS", ItemClassification.filler),
    DungeonItemData(ItemName.COMPASS1, "COMPASS1", ItemClassification.filler),
    DungeonItemData(ItemName.COMPASS2, "COMPASS2", ItemClassification.filler),
    DungeonItemData(ItemName.COMPASS3, "COMPASS3", ItemClassification.filler),
    DungeonItemData(ItemName.COMPASS4, "COMPASS4", ItemClassification.filler),
    DungeonItemData(ItemName.COMPASS5, "COMPASS5", ItemClassification.filler),
    DungeonItemData(ItemName.COMPASS6, "COMPASS6", ItemClassification.filler),
    DungeonItemData(ItemName.COMPASS7, "COMPASS7", ItemClassification.filler),
    DungeonItemData(ItemName.COMPASS8, "COMPASS8", ItemClassification.filler),
    DungeonItemData(ItemName.COMPASS9, "COMPASS9", ItemClassification.filler),
    #DungeonItemData(ItemName.STONE_BEAK, "STONE_BEAK", ItemClassification.filler),
    DungeonItemData(ItemName.STONE_BEAK1, "STONE_BEAK1", ItemClassification.filler),
    DungeonItemData(ItemName.STONE_BEAK2, "STONE_BEAK2", ItemClassification.filler),
    DungeonItemData(ItemName.STONE_BEAK3, "STONE_BEAK3", ItemClassification.filler),
    DungeonItemData(ItemName.STONE_BEAK4, "STONE_BEAK4", ItemClassification.filler),
    DungeonItemData(ItemName.STONE_BEAK5, "STONE_BEAK5", ItemClassification.filler),
    DungeonItemData(ItemName.STONE_BEAK6, "STONE_BEAK6", ItemClassification.filler),
    DungeonItemData(ItemName.STONE_BEAK7, "STONE_BEAK7", ItemClassification.filler),
    DungeonItemData(ItemName.STONE_BEAK8, "STONE_BEAK8", ItemClassification.filler),
    DungeonItemData(ItemName.STONE_BEAK9, "STONE_BEAK9", ItemClassification.filler),
    ItemData(ItemName.SONG1, "SONG1", ItemClassification.progression),
    ItemData(ItemName.SONG2, "SONG2", ItemClassification.useful),
    ItemData(ItemName.SONG3, "SONG3", ItemClassification.progression),  # TODO
    DungeonItemData(ItemName.INSTRUMENT1, "INSTRUMENT1", ItemClassification.progression),
    DungeonItemData(ItemName.INSTRUMENT2, "INSTRUMENT2", ItemClassification.progression),
    DungeonItemData(ItemName.INSTRUMENT3, "INSTRUMENT3", ItemClassification.progression),
    DungeonItemData(ItemName.INSTRUMENT4, "INSTRUMENT4", ItemClassification.progression),
    DungeonItemData(ItemName.INSTRUMENT5, "INSTRUMENT5", ItemClassification.progression),
    DungeonItemData(ItemName.INSTRUMENT6, "INSTRUMENT6", ItemClassification.progression),
    DungeonItemData(ItemName.INSTRUMENT7, "INSTRUMENT7", ItemClassification.progression),
    DungeonItemData(ItemName.INSTRUMENT8, "INSTRUMENT8", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_YOSHI_DOLL, "TRADING_ITEM_YOSHI_DOLL", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_RIBBON, "TRADING_ITEM_RIBBON", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_DOG_FOOD, "TRADING_ITEM_DOG_FOOD", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_BANANAS, "TRADING_ITEM_BANANAS", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_STICK, "TRADING_ITEM_STICK", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_HONEYCOMB, "TRADING_ITEM_HONEYCOMB", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_PINEAPPLE, "TRADING_ITEM_PINEAPPLE", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_HIBISCUS, "TRADING_ITEM_HIBISCUS", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_LETTER, "TRADING_ITEM_LETTER", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_BROOM, "TRADING_ITEM_BROOM", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_FISHING_HOOK, "TRADING_ITEM_FISHING_HOOK", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_NECKLACE, "TRADING_ITEM_NECKLACE", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_SCALE, "TRADING_ITEM_SCALE", ItemClassification.progression),
    ItemData(ItemName.TRADING_ITEM_MAGNIFYING_GLASS, "TRADING_ITEM_MAGNIFYING_GLASS", ItemClassification.progression)
]

ladxr_item_to_la_item_name = {
    item.ladxr_id: item.item_name for item in links_awakening_items
}

links_awakening_items_by_name = {
    item.item_name : item for item in links_awakening_items
}

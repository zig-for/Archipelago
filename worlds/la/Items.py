from BaseClasses import Item
from Common import *
import typing

class ItemData(typing.NamedTuple):
    item_id: int
    progression: bool
class LinksAwakeningItem(Item):
    game: str = LINKS_AWAKENING

class Item:
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
    RUPEES_50 = "Rupees 50"
    RUPEES_20 = "Rupees 20"
    RUPEES_100 = "Rupees 100"
    RUPEES_200 = "Rupees 200"
    RUPEES_500 = "Rupees 500"
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

UNIMPLEMENTED  =  0
item_table = {
    Item.POWER_BRACELET: ItemData(UNIMPLEMENTED, True),
    Item.SHIELD: ItemData(UNIMPLEMENTED, True),
    Item.BOW: ItemData(UNIMPLEMENTED, True),
    Item.HOOKSHOT: ItemData(UNIMPLEMENTED, True),
    Item.MAGIC_ROD: ItemData(UNIMPLEMENTED, True),
    Item.PEGASUS_BOOTS: ItemData(UNIMPLEMENTED, True),
    Item.OCARINA: ItemData(UNIMPLEMENTED, True),
    Item.FEATHER: ItemData(UNIMPLEMENTED, True),
    Item.SHOVEL: ItemData(UNIMPLEMENTED, True),
    Item.MAGIC_POWDER: ItemData(UNIMPLEMENTED, True),
    Item.BOMB: ItemData(UNIMPLEMENTED, True),
    Item.SWORD: ItemData(UNIMPLEMENTED, True),
    Item.FLIPPERS: ItemData(UNIMPLEMENTED, True),
    Item.MAGNIFYING_LENS: ItemData(UNIMPLEMENTED, True),
    Item.MEDICINE: ItemData(UNIMPLEMENTED, True),
    Item.TAIL_KEY: ItemData(UNIMPLEMENTED, True),
    Item.ANGLER_KEY: ItemData(UNIMPLEMENTED, True),
    Item.FACE_KEY: ItemData(UNIMPLEMENTED, True),
    Item.BIRD_KEY: ItemData(UNIMPLEMENTED, True),
    Item.SLIME_KEY: ItemData(UNIMPLEMENTED, True),
    Item.GOLD_LEAF: ItemData(UNIMPLEMENTED, True),
    Item.RUPEES_50: ItemData(UNIMPLEMENTED, False),
    Item.RUPEES_20: ItemData(UNIMPLEMENTED, False),
    Item.RUPEES_100: ItemData(UNIMPLEMENTED, False),
    Item.RUPEES_200: ItemData(UNIMPLEMENTED, False),
    Item.RUPEES_500: ItemData(UNIMPLEMENTED, False),
    Item.SEASHELL: ItemData(UNIMPLEMENTED, True),
    Item.MESSAGE: ItemData(UNIMPLEMENTED, True),
    Item.GEL: ItemData(UNIMPLEMENTED, True),
    Item.BOOMERANG: ItemData(UNIMPLEMENTED, True),
    Item.HEART_PIECE: ItemData(UNIMPLEMENTED, True),
    Item.BOWWOW: ItemData(UNIMPLEMENTED, True),
    Item.ARROWS_10: ItemData(UNIMPLEMENTED, True),
    Item.SINGLE_ARROW: ItemData(UNIMPLEMENTED, False),
    Item.ROOSTER: ItemData(UNIMPLEMENTED, True),
    Item.MAX_POWDER_UPGRADE: ItemData(UNIMPLEMENTED, False),
    Item.MAX_BOMBS_UPGRADE: ItemData(UNIMPLEMENTED, False),
    Item.MAX_ARROWS_UPGRADE: ItemData(UNIMPLEMENTED, False),
    Item.RED_TUNIC: ItemData(UNIMPLEMENTED, True),
    Item.BLUE_TUNIC: ItemData(UNIMPLEMENTED, True),
    Item.HEART_CONTAINER: ItemData(UNIMPLEMENTED, True),
    Item.BAD_HEART_CONTAINER: ItemData(UNIMPLEMENTED, True),
    Item.TOADSTOOL: ItemData(UNIMPLEMENTED, True),
    Item.KEY: ItemData(UNIMPLEMENTED, True),
    Item.KEY1: ItemData(UNIMPLEMENTED, True),
    Item.KEY2: ItemData(UNIMPLEMENTED, True),
    Item.KEY3: ItemData(UNIMPLEMENTED, True),
    Item.KEY4: ItemData(UNIMPLEMENTED, True),
    Item.KEY5: ItemData(UNIMPLEMENTED, True),
    Item.KEY6: ItemData(UNIMPLEMENTED, True),
    Item.KEY7: ItemData(UNIMPLEMENTED, True),
    Item.KEY8: ItemData(UNIMPLEMENTED, True),
    Item.KEY9: ItemData(UNIMPLEMENTED, True),
    Item.NIGHTMARE_KEY: ItemData(UNIMPLEMENTED, True),
    Item.NIGHTMARE_KEY1: ItemData(UNIMPLEMENTED, True),
    Item.NIGHTMARE_KEY2: ItemData(UNIMPLEMENTED, True),
    Item.NIGHTMARE_KEY3: ItemData(UNIMPLEMENTED, True),
    Item.NIGHTMARE_KEY4: ItemData(UNIMPLEMENTED, True),
    Item.NIGHTMARE_KEY5: ItemData(UNIMPLEMENTED, True),
    Item.NIGHTMARE_KEY6: ItemData(UNIMPLEMENTED, True),
    Item.NIGHTMARE_KEY7: ItemData(UNIMPLEMENTED, True),
    Item.NIGHTMARE_KEY8: ItemData(UNIMPLEMENTED, True),
    Item.NIGHTMARE_KEY9: ItemData(UNIMPLEMENTED, True),
    Item.MAP: ItemData(UNIMPLEMENTED, False),
    Item.MAP1: ItemData(UNIMPLEMENTED, False),
    Item.MAP2: ItemData(UNIMPLEMENTED, False),
    Item.MAP3: ItemData(UNIMPLEMENTED, False),
    Item.MAP4: ItemData(UNIMPLEMENTED, False),
    Item.MAP5: ItemData(UNIMPLEMENTED, False),
    Item.MAP6: ItemData(UNIMPLEMENTED, False),
    Item.MAP7: ItemData(UNIMPLEMENTED, False),
    Item.MAP8: ItemData(UNIMPLEMENTED, False),
    Item.MAP9: ItemData(UNIMPLEMENTED, False),
    Item.COMPASS: ItemData(UNIMPLEMENTED, False),
    Item.COMPASS1: ItemData(UNIMPLEMENTED, False),
    Item.COMPASS2: ItemData(UNIMPLEMENTED, False),
    Item.COMPASS3: ItemData(UNIMPLEMENTED, False),
    Item.COMPASS4: ItemData(UNIMPLEMENTED, False),
    Item.COMPASS5: ItemData(UNIMPLEMENTED, False),
    Item.COMPASS6: ItemData(UNIMPLEMENTED, False),
    Item.COMPASS7: ItemData(UNIMPLEMENTED, False),
    Item.COMPASS8: ItemData(UNIMPLEMENTED, False),
    Item.COMPASS9: ItemData(UNIMPLEMENTED, False),
    Item.STONE_BEAK: ItemData(UNIMPLEMENTED, False),
    Item.STONE_BEAK1: ItemData(UNIMPLEMENTED, False),
    Item.STONE_BEAK2: ItemData(UNIMPLEMENTED, False),
    Item.STONE_BEAK3: ItemData(UNIMPLEMENTED, False),
    Item.STONE_BEAK4: ItemData(UNIMPLEMENTED, False),
    Item.STONE_BEAK5: ItemData(UNIMPLEMENTED, False),
    Item.STONE_BEAK6: ItemData(UNIMPLEMENTED, False),
    Item.STONE_BEAK7: ItemData(UNIMPLEMENTED, False),
    Item.STONE_BEAK8: ItemData(UNIMPLEMENTED, False),
    Item.STONE_BEAK9: ItemData(UNIMPLEMENTED, False),
    Item.SONG1: ItemData(UNIMPLEMENTED, True), 
    Item.SONG2: ItemData(UNIMPLEMENTED, True), # TODO
    Item.SONG3: ItemData(UNIMPLEMENTED, True), # TODO
    Item.INSTRUMENT1: ItemData(UNIMPLEMENTED, True),
    Item.INSTRUMENT2: ItemData(UNIMPLEMENTED, True),
    Item.INSTRUMENT3: ItemData(UNIMPLEMENTED, True),
    Item.INSTRUMENT4: ItemData(UNIMPLEMENTED, True),
    Item.INSTRUMENT5: ItemData(UNIMPLEMENTED, True),
    Item.INSTRUMENT6: ItemData(UNIMPLEMENTED, True),
    Item.INSTRUMENT7: ItemData(UNIMPLEMENTED, True),
    Item.INSTRUMENT8: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_YOSHI_DOLL: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_RIBBON: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_DOG_FOOD: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_BANANAS: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_STICK: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_HONEYCOMB: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_PINEAPPLE: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_HIBISCUS: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_LETTER: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_BROOM: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_FISHING_HOOK: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_NECKLACE: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_SCALE: ItemData(UNIMPLEMENTED, True),
    Item.TRADING_ITEM_MAGNIFYING_GLASS: ItemData(UNIMPLEMENTED, True)
}

# TODO
item_frequences = {
    Item.KEY: 1,
    Item.KEY1: 1,
    Item.KEY2: 1,
    Item.KEY3: 1,
    Item.KEY4: 1,
    Item.KEY5: 1,
    Item.KEY6: 1,
    Item.KEY7: 1,
    Item.KEY8: 1,
    Item.KEY9: 1,
}
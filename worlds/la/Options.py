import typing
from Options import Choice, Option, Toggle, DefaultOnToggle, Range

DefaultOffToggle = Toggle

class Logic(Choice):
    """Affects where items are allowed to be placed.
    [Casual] Same as normal, except that a few more complex options are removed, like removing bushes with powder and killing enemies with powder or bombs.
    [Normal] playable without using any tricks or glitches. Requires nothing to be done outside of normal item usage.
    [Hard] More advanced techniques may be required, but glitches are not. Examples include tricky jumps, killing enemies with only pots and skipping keys with smart routing.
    [Glitched] Advanced glitches and techniques may be required, but extremely difficult or tedious tricks are not required. Examples include Bomb Triggers, Super Jumps and Jesus Jumps.
    [Hell] Obscure and hard techniques may be required. Examples include featherless jumping with boots and/or hookshot, sequential pit buffers and unclipped superjumps. Things in here can be extremely hard to do or very time consuming."""
    display_name = "Logic"
    casual = 0
    normal = 1
    hard = 2
    glitched = 3
    hell = 4
    
    default = normal
    
#            Setting('forwardfactor', 'Main', 'F', 'Forward Factor', default=0.0,
#                description="Forward item weight adjustment factor, lower values generate more rear heavy seeds while higher values generate front heavy seeds. Default is 0.5."),
#            Setting('accessibility', 'Main', 'A', 'Accessibility', options=[('all', 'a', '100% Locations'), ('goal', 'g', 'Beatable')], default='all',
#                description="""
#[100% Locations] guaranteed that every single item can be reached and gained.
#[Beatable] only guarantees that the game is beatable. Certain items/chests might never be reachable."""),
#            Setting('race', 'Main', 'V', 'Race mode', default=False, multiworld=False,
#                description="""
#Spoiler logs can not be generated for ROMs generated with race mode enabled, and seed generation is slightly different."""),
#             Setting('spoilerformat', 'Main', 'Spoiler Format', options=[('none', 'None'), ('text', 'Text'), ('json', 'JSON')], default='none', multiworld=False,
#                 description="""Affects how the spoiler log is generated.
# [None] No spoiler log is generated. One can still be manually dumped later.
# [Text] Creates a .txt file meant for a human to read.
# [JSON] Creates a .json file with a little more information and meant for a computer to read.""")


class Boomerang(Choice):
    """
    [Normal], requires magnifier to get the boomerang.
    [Trade], allows to trade an inventory item for a random other inventory item boomerang is shuffled.
    [Gift], You get a random gift of any item, and the boomerang is shuffled.
    """

    normal = 0
    trade = 1
    gift = 2
    default = gift

# TODO: I know we have helper classes for this
# this is the worst way to do this but I'm mechanically translating to Archipelago parlance
# Break apart before merge
class DungeonItemsShuffle(Choice):
    """Sets if dungeon items can only be in their respective dungeon, or everywhere.
    [Standard] dungeon items are only in their dungeon.
    [Maps/.../..] specified items can be anywhere
    [Keysanity] all dungeon items can be anywhere.
    [Keysy] no keys, key doors are already open."""
    standard = 0
    smallkeys = 1
    localkeys = 2
    localnightmarekey = 3
    keysanity = 4
    kysy = 5

    default = standard

# TODO: translate to lttp parlance
class EntranceShuffle(Choice):
    """Randomizes where overworld entrances lead to.
    [Simple] single entrance caves that contain items are randomized
    [Advanced] Connector caves are also randomized
    [Expert] Caves/houses without items are also randomized
    [Insanity] A few very annoying entrances will be randomized as well.
    If random start location and/or dungeon shuffle is enabled, then these will be shuffled with all the entrances.
    Note, some entrances can lead into water, use the warp-to-home from the save&quit menu to escape this."""
    none = 0
    simple = 1
    advanced = 2
    expert = 3    
    insanity = 4
    default = none

class BossShuffle(Choice):
    none = 0
    shuffle = 1
    random = 2
    default = none


class Goal(Choice):
    todo = 0
    default = todo
#             Setting('goal', 'Gameplay', 'G', 'Goal', options=[('8', '8', '8 instruments'), ('7', '7', '7 instruments'), ('6', '6', '6 instruments'),
#                                                          ('5', '5', '5 instruments'), ('4', '4', '4 instruments'), ('3', '3', '3 instruments'),
#                                                          ('2', '2', '2 instruments'), ('1', '1', '1 instrument'), ('0', '0', 'No instruments'),
#                                                          ('open', 'O', 'Egg already open'), ('random', 'R', 'Random instrument count'),
#                                                          ('open-4', '<', 'Random short game (0-4)'), ('5-8', '>', 'Random long game (5-8)'),
#                                                          ('seashells', 'S', 'Seashell hunt (20)'), ('bingo', 'b', 'Bingo!'),
#                                                          ('bingo-full', 'B', 'Bingo-25!')], default='8',
#                 description="""Changes the goal of the game.
# [1-8 instruments], number of instruments required to open the egg.
# [No instruments] open the egg without instruments, still requires the ocarina with the balled of the windfish
# [Egg already open] the egg is already open, just head for it once you have the items needed to defeat the boss.
# [Randomized instrument count] random number of instruments required to open the egg, between 0 and 8.
# [Random short/long game] random number of instruments required to open the egg, chosen between 0-4 and 5-8 respectively.
# [Seashell hunt] egg will open once you collected 20 seashells. Instruments are replaced by seashells and shuffled.
# [Bingo] Generate a 5x5 bingo board with various goals. Complete one row/column or diagonal to win!
# [Bingo-25] Bingo, but need to fill the whole bingo card to win!"""),
class ItemPool(Choice):
    """Effects which items are shuffled.
[Casual] places more inventory and key items so the seed is easier.
[More keys] adds more small keys and extra nightmare keys so dungeons are easier.
[Path of pain]... just find out yourself."""
    casual = 0
    more_keys = 1
    normal = 2
    painful = 3
    default = normal

#             Setting('hpmode', 'Gameplay', 'm', 'Health mode', options=[('default', '', 'Normal'), ('inverted', 'i', 'Inverted'), ('1', '1', 'Start with 1 heart'), ('low', 'l', 'Low max')], default='default',
#                 description="""
# [Normal} health works as you would expect.
# [Inverted] you start with 9 heart containers, but killing a boss will take a heartcontainer instead of giving one.
# [Start with 1] normal game, you just start with 1 heart instead of 3.
# [Low max] replace heart containers with heart pieces."""),

#             Setting('hardmode', 'Gameplay', 'X', 'Hard mode', options=[('none', '', 'Disabled'), ('oracle', 'O', 'Oracle'), ('hero', 'H', 'Hero'), ('ohko', '1', 'One hit KO')], default='none',
#                 description="""
# [Oracle] Less iframes and heath from drops. Bombs damage yourself. Water damages you without flippers. No piece of power or acorn.
# [Hero] Switch version hero mode, double damage, no heart/fairy drops.
# [One hit KO] You die on a single hit, always."""),

#             Setting('steal', 'Gameplay', 't', 'Stealing from the shop',
#                 options=[('always', 'a', 'Always'), ('never', 'n', 'Never'), ('default', '', 'Normal')], default='default',
#                 description="""Effects when you can steal from the shop. Stealing is bad and never in logic.
# [Normal] requires the sword before you can steal.
# [Always] you can always steal from the shop
# [Never] you can never steal from the shop."""),
class Bowwow(Choice):
    """Allows BowWow to be taken into any area, damage bosses and more enemies. If enabled you always start with bowwow. Swordless option removes the swords from the game and requires you to beat the game without a sword and just bowwow."""
    normal = 0
    always = 1
    swordless = 2
    default = normal

class Overworld(Choice):
    """
    [Dungeon Dive] Create a different overworld where all the dungeons are directly accessible and almost no chests are located in the overworld.
    [No dungeons] All dungeons only consist of a boss fight and a instrument reward. Rest of the dungeon is removed.
    """
    normal = 0
    dungeon_dive = 1
    tiny_dungeons = 2
    default = normal
# Ugh, this will change what 'progression' means??
#Setting('owlstatues', 'Special', 'o', 'Owl statues', options=[('', '', 'Never'), ('dungeon', 'D', 'In dungeons'), ('overworld', 'O', 'On the overworld'), ('both', 'B', 'Dungeons and Overworld')], default='',
#    description='Replaces the hints from owl statues with additional randomized items'),

#Setting('superweapons', 'Special', 'q', 'Enable super weapons', default=False,
#    description='All items will be more powerful, faster, harder, bigger stronger. You name it.'),
#Setting('quickswap', 'User options', 'Q', 'Quickswap', options=[('none', '', 'Disabled'), ('a', 'a', 'Swap A button'), ('b', 'b', 'Swap B button')], default='none',
#    description='Adds that the select button swaps with either A or B. The item is swapped with the top inventory slot. The map is not available when quickswap is enabled.',
#    aesthetic=True),
#             Setting('textmode', 'User options', 'f', 'Text mode', options=[('fast', '', 'Fast'), ('default', 'd', 'Normal'), ('none', 'n', 'No-text')], default='fast',
#                 description="""[Fast] makes text appear twice as fast.
# [No-Text] removes all text from the game""", aesthetic=True),
#             Setting('lowhpbeep', 'User options', 'p', 'Low HP beeps', options=[('none', 'D', 'Disabled'), ('slow', 'S', 'Slow'), ('default', 'N', 'Normal')], default='slow',
#                 description='Slows or disables the low health beeping sound', aesthetic=True),
#             Setting('noflash', 'User options', 'l', 'Remove flashing lights', default=True,
#                 description='Remove the flashing light effects from Mamu, shopkeeper and MadBatter. Useful for capture cards and people that are sensitive for these things.',
#                 aesthetic=True),
#             Setting('nagmessages', 'User options', 'S', 'Show nag messages', default=False,
#                 description='Enables the nag messages normally shown when touching stones and crystals',
#                 aesthetic=True),
#             Setting('gfxmod', 'User options', 'c', 'Graphics', options=gfx_options, default='',
#                 description='Generally affects at least Link\'s sprite, but can alter any graphics in the game',
#                 aesthetic=True),
#             Setting('linkspalette', 'User options', 'C', "Link's color",
#                 options=[('-1', '-', 'Normal'), ('0', '0', 'Green'), ('1', '1', 'Yellow'), ('2', '2', 'Red'), ('3', '3', 'Blue'),
#                          ('4', '4', '?? A'), ('5', '5', '?? B'), ('6', '6', '?? C'), ('7', '7', '?? D')], default='-1', aesthetic=True,
#                 description="""Allows you to force a certain color on link.
# [Normal] color of link depends on the tunic.
# [Green/Yellow/Red/Blue] forces link into one of these colors.
# [?? A/B/C/D] colors of link are usually inverted and color depends on the area you are in."""),
#             Setting('music', 'User options', 'M', 'Music', options=[('', '', 'Default'), ('random', 'r', 'Random'), ('off', 'o', 'Disable')], default='',
#                 description="""
# [Random] Randomizes overworld and dungeon music'
# [Disable] no music in the whole game""",
#                 aesthetic=True),


links_awakening_options: typing.Dict[str, typing.Type[Option]] = {
    # 'logic': Logic,
    # 'heartpiece': DefaultOnToggle, # description='Includes heart pieces in the item pool'),                
    # 'seashells': DefaultOnToggle, # description='Randomizes the secret sea shells hiding in the ground/trees. (chest are always randomized)'),                
    # 'heartcontainers': DefaultOnToggle, # description='Includes boss heart container drops in the item pool'),                
    # 'instruments': DefaultOffToggle, # description='Instruments are placed on random locations, dungeon goal will just contain a random item.'),                
    # 'tradequest': DefaultOnToggle, # description='Trade quest items are randomized, each NPC takes its normal trade quest item, but gives a random item'),                
    # 'witch': DefaultOnToggle, # description='Adds both the toadstool and the reward for giving the toadstool to the witch to the item pool'),                
    # 'rooster': DefaultOnToggle, # description='Adds the rooster to the item pool. Without this option, the rooster spot is still a check giving an item. But you will never find the rooster. Any rooster spot is accessible without rooster by other means.'),                
    # 'boomerang': Boomerang,
    # 'dungeonitemshuffle': DungeonItemsShuffle,
    # 'randomstartlocation': DefaultOffToggle, # 'Randomize where your starting house is located'),
    # 'dungeonshuffle': DefaultOffToggle, # 'Randomizes the dungeon that each dungeon entrance leads to'),
    # 'entranceshuffle': EntranceShuffle,
    # 'bossshuffle': BossShuffle,
    # 'minibossshuffle': BossShuffle,
    # 'goal': Goal,
    # 'itempool': ItemPool,
    # 'bowwow': Bowwow,
    # 'overworld': Overworld,
}

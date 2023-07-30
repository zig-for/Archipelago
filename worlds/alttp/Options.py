from __future__ import annotations
import typing

from BaseClasses import MultiWorld
from Options import (Choice, DeathLink, DefaultOnToggle, FreeText,
                     Option, PlandoBosses, Range,
                     StartInventoryPool, Toggle)


class Logic(Choice):
    # TODO: text
    """
    No Glitches:
    Minor Glitches: May require Fake Flippers, Bunny Revival
                    and Dark Room Navigation.
    Overworld Glitches: May require overworld glitches.
    Hybrid Major Glitches: May require both overworld and underworld clipping. 
    No Logic: Distribute items without regard for
                    item requirements.
                             """
    # TODO: go back and replace these to underscore versions
    option_noglitches = 0
    option_minorglitches = 1
    option_owglitches = 2
    option_hybridglitches = 3
    option_nologic = 4
    alias_owg = option_owglitches
    alias_hmg = option_hybridglitches
    alias_no_logic = option_nologic
    alias_overworld_glitches = option_owglitches
    alias_minor_glitches = option_minorglitches
    alias_hybrid_major_glitches = option_hybridglitches

    
class Goal(Choice):
    # TODO
    """
    ganon:         Collect all crystals, beat Agahnim 2 then
                   defeat Ganon.
    crystals:      Collect all crystals then defeat Ganon.
    pedestal:      Places the Triforce at the Master Sword Pedestal.
    ganonpedestal: Pull the Master Sword Pedestal, then defeat Ganon.
    bosses:        Collect all crystals, pendants, beat both
                   Agahnim fights and then defeat Ganon.
    triforcehunt: Places 30 Triforce Pieces in the world, collect
                   20 of them to beat the game.
    local: Places 30 Triforce Pieces in your world, collect
                   20 of them to beat the game.
    ganontriforcehunt: Places 30 Triforce Pieces in the world, collect
                   20 of them, then defeat Ganon.
    localganontriforcehunt: Places 30 Triforce Pieces in your world,
                   collect 20 of them, then defeat Ganon.
    """
    option_ganon = 0
    option_pedestal = 1
    option_bosses = 2
    option_triforcehunt = 3
    option_localtriforcehunt = 4
    option_ganontriforcehunt = 5
    option_localganontriforcehunt = 6
    option_crystals = 7
    option_ganonpedestal = 8
    option_icerodhunt = 9

    def is_triforce_hunt(self) -> bool:
        return self.value in [Goal.option_triforcehunt,
                              Goal.option_localtriforcehunt,
                              Goal.option_ganontriforcehunt,
                              Goal.option_localganontriforcehunt]
    
    def is_local_triforce_hunt(self) -> bool:
        return self.value in [Goal.option_localtriforcehunt,
                              Goal.option_localganontriforcehunt]

class Timer(Choice):
    option_none = 0
    option_display = 1
    option_timed = 2
    option_timed_ohko = 3
    option_ohko = 4
    option_timed_countdown = 5
#setattr(Timer, "alias_timed-ohko", Timer.option_timed_ohko)
#setattr(Timer, "alias_timed-countdown", Timer.option_timed_countdown)

class CountdownStartTime(Range):
    range_start = 0
    range_end = 10000
    """Set amount of time, in minutes, to start with in Timed Countdown and Timed OHKO modes"""
    default = 10

class ClockTime(Range):
    range_start = -10000
    range_end = 10000

class RedClockTime(ClockTime):
    """For all timer modes, the amount of time in minutes to gain or lose when picking up a red clock"""
    default = -2

class BlueClockTime(ClockTime):
    """For all timer modes, the amount of time in minutes to gain or lose when picking up a blue clock"""
    default = 2

class GreenClockTime(ClockTime):
    """For all timer modes, the amount of time in minutes to gain or lose when picking up a green clock"""
    default = 4


class Mode(Choice):
    option_standard = 0
    option_open = 1
    option_inverted = 2
    default = option_standard

class DungeonCounters(Choice):
    option_off = 0
    option_pickup = 1
    option_on = 2
    default = option_pickup
    
class OpenPyramid(Choice):
    """Determines whether the hole at the top of pyramid is open.
    Goal will open the pyramid if the goal requires you to kill Ganon, without needing to kill Agahnim 2.
    Auto is the same as goal except if Ganon's dropdown is in another location, the hole will be closed."""
    display_name = "Open Pyramid Hole"
    option_closed = 0
    option_open = 1
    option_goal = 2
    option_auto = 3
    default = option_goal

    alias_true = option_open
    alias_false = option_closed

    def to_bool(self, world: MultiWorld, player: int) -> bool:
        if self.value == self.option_goal:
            return world.goal[player] in {Goal.option_crystals, Goal.option_ganontriforcehunt, Goal.option_localganontriforcehunt, Goal.option_ganonpedestal}
        elif self.value == self.option_auto:
            return world.goal[player] in {Goal.option_crystals, Goal.option_ganontriforcehunt, Goal.option_localganontriforcehunt, Goal.option_ganonpedestal} \
            and (world.shuffle[player] in {EntranceShuffle.option_vanilla, EntranceShuffle.option_dungeonssimple, EntranceShuffle.option_dungeonsfull, EntranceShuffle.option_dungeonscrossed} or not
                 world.shuffle_ganon)
        elif self.value == self.option_open:
            return True
        else:
            return False

class Sprite(FreeText):
    """
    TODO: probably broke this
    """

class DungeonItem(Choice):
    value: int
    option_original_dungeon = 0
    option_own_dungeons = 1
    option_own_world = 2
    option_any_world = 3
    option_different_world = 4
    option_start_with = 6
    alias_true = 3
    alias_false = 0

    @property
    def in_dungeon(self):
        return self.value in {0, 1}

    @property
    def hints_useful(self):
        """Indicates if hints for this Item are useful in any way."""
        return self.value in {1, 2, 3, 4}


class bigkey_shuffle(DungeonItem):
    """Big Key Placement"""
    item_name_group = "Big Keys"
    display_name = "Big Key Shuffle"


class smallkey_shuffle(DungeonItem):
    """Small Key Placement"""
    option_universal = 5
    item_name_group = "Small Keys"
    display_name = "Small Key Shuffle"


class compass_shuffle(DungeonItem):
    """Compass Placement"""
    item_name_group = "Compasses"
    display_name = "Compass Shuffle"


class map_shuffle(DungeonItem):
    """Map Placement"""
    item_name_group = "Maps"
    display_name = "Map Shuffle"


class Crystals(Range):
    range_start = 0
    range_end = 7


class CrystalsTower(Crystals):
    """Number of crystals needed to open Ganon's Tower"""
    display_name = "Crystals for GT"
    default = 7


class CrystalsGanon(Crystals):
    """Number of crystals needed to damage Ganon"""
    display_name = "Crystals for Ganon"
    default = 7


class TriforcePieces(Range):
     default = 30
     range_start = 1
     range_end = 90

class TriforcePiecesMode(Choice):
    #Determine how to calculate the extra available triforce pieces.
    option_extra = 0 # available = triforce_pieces_extra + triforce_pieces_required
    option_percentage = 1 # available = (triforce_pieces_percentage /100) * triforce_pieces_required
    option_available = 2 # available = triforce_pieces_available
    default = option_available

class TriforcePiecesAvailable(TriforcePieces):
    pass

class TriforcePiecesRequired(TriforcePieces):
    default = 20

class TriforcePiecesExtra(TriforcePieces):
    default = 10
    
class TriforcePiecesPercentage(Range):
    # ???
    range_start = 100
    range_end = 500
    default = 150

class ShopItemSlots(Range):
    """Number of slots in all shops available to have items from the multiworld"""
    display_name = "Available Shop Slots"
    range_start = 0
    range_end = 30


class ShopPriceModifier(Range):
    """Percentage modifier for shuffled item prices in shops"""
    display_name = "Shop Price Cost Percent"
    range_start = 0
    default = 100
    range_end = 400


class WorldState(Choice):
    option_standard = 1
    option_open = 0
    option_inverted = 2


class Difficulty(Choice):
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3
    default = option_normal

class ItemFunctionality(Choice):
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3
    default = option_normal

class LTTPBosses(PlandoBosses):
    """Shuffles bosses around to different locations.
    Basic will shuffle all bosses except Ganon and Agahnim anywhere they can be placed.
    Full chooses 3 bosses at random to be placed twice instead of Lanmolas, Moldorm, and Helmasaur.
    Chaos allows any boss to appear any number of times.
    Singularity places a single boss in as many places as possible, and a second boss in any remaining locations.
    Supports plando placement."""
    display_name = "Boss Shuffle"
    option_none = 0
    option_basic = 1
    option_full = 2
    option_chaos = 3
    option_singularity = 4

    duplicate_bosses = True

    bosses = {
        "Armos Knights",
        "Lanmolas",
        "Moldorm",
        "Helmasaur King",
        "Arrghus",
        "Mothula",
        "Blind",
        "Kholdstare",
        "Vitreous",
        "Trinexx",
    }

    locations = {
        "Ganons Tower Top",
        "Tower of Hera",
        "Skull Woods",
        "Ganons Tower Middle",
        "Eastern Palace",
        "Desert Palace",
        "Palace of Darkness",
        "Swamp Palace",
        "Thieves Town",
        "Ice Palace",
        "Misery Mire",
        "Turtle Rock",
        "Ganons Tower Bottom"
    }

    @classmethod
    def can_place_boss(cls, boss: str, location: str) -> bool:
        from worlds.alttp.Bosses import can_place_boss
        level = ''
        words = location.split(" ")
        if words[-1] in ("top", "middle", "bottom"):
            level = words[-1]
            location = " ".join(words[:-1])
        location = location.title().replace("Of", "of")
        return can_place_boss(boss.title(), location, level)


class Enemies(Choice):
    option_vanilla = 0
    option_shuffled = 1
    option_chaos = 2


class Progressive(Choice):
    """How item types that have multiple tiers (armor, bows, gloves, shields, and swords) should be rewarded"""
    display_name = "Progressive Items"
    option_off = 0
    option_grouped_random = 1
    option_on = 2
    default = 2

    def want_progressives(self, random):
        return random.choice([True, False]) if self.value == self.option_grouped_random else bool(self.value)


class EntranceShuffle(Choice):
    option_vanilla = 0
    option_simple = 1
    option_restricted = 2
    option_full = 3
    option_crossed = 4
    option_insanity = 5
    option_madness = 6
    option_dungeonsfull = 7
    option_dungeonssimple = 8
    option_dungeonscrossed = 9
    option_restricted_legacy = -1
    option_full_legacy = -2
    option_madness_legacy = -3
    option_insanity_legacy = -4

    er_seed: str = ''

    @classmethod
    def from_text(cls, text: str) -> EntranceShuffle:
        if "-" in text:
            shuffle, seed = text.split("-", 1)  
        else:
            shuffle, seed = text, ''
        ret = super().from_text(shuffle)
        assert(type(ret) is EntranceShuffle)
        if ret == EntranceShuffle.option_vanilla:
            seed = 'vanilla'

        ret.er_seed = seed  

        return ret

class Swordless(Toggle):
    """No swords. Curtains in Skull Woods and Agahnim's
    Tower are removed, Agahnim's Tower barrier can be
    destroyed with hammer. Misery Mire and Turtle Rock
    can be opened without a sword. Hammer damages Ganon.
    Ether and Bombos Tablet can be activated with Hammer
    (and Book)."""
    display_name = "Swordless"


# Might be a decent idea to split "Bow" into its own option with choices of
# Defer to Progressive Option (default), Progressive, Non-Progressive, Bow + Silvers, Retro
class RetroBow(Toggle):
    """Zelda-1 like mode. You have to purchase a quiver to shoot arrows using rupees."""
    display_name = "Retro Bow"


class RetroCaves(Toggle):
    """Zelda-1 like mode. There are randomly placed take-any caves that contain one Sword and
    choices of Heart Container/Blue Potion."""
    display_name = "Retro Caves"


class RestrictBossItem(Toggle):
    """Don't place dungeon-native items on the dungeon's boss."""
    display_name = "Prevent Dungeon Item on Boss"


class Hints(Choice):
    """On/Full: Put item and entrance placement hints on telepathic tiles and some NPCs, Full removes joke hints."""
    display_name = "Hints"
    option_off = 0
    option_on = 2
    option_full = 3
    default = 2


class Scams(Choice):
    """If on, these Merchants will no longer tell you what they're selling."""
    display_name = "Scams"
    option_off = 0
    option_king_zora = 1
    option_bottle_merchant = 2
    option_all = 3

    @property
    def gives_king_zora_hint(self):
        return self.value in {0, 2}

    @property
    def gives_bottle_merchant_hint(self):
        return self.value in {0, 1}


class EnemyShuffle(Toggle):
    """Randomize every enemy spawn.
    If mode is Standard, Hyrule Castle is left out (may result in visually wrong enemy sprites in that area.)"""
    display_name = "Enemy Shuffle"


class KillableThieves(Toggle):
    """Makes Thieves killable."""
    display_name = "Killable Thieves"


class BushShuffle(Toggle):
    """Randomize chance that a bush contains an enemy as well as which enemy may spawn."""
    display_name = "Bush Shuffle"


class TileShuffle(Toggle):
    """Randomize flying tiles floor patterns."""
    display_name = "Tile Shuffle"


class PotShuffle(Toggle):
    """Shuffle contents of pots within "supertiles" (item will still be nearby original placement)."""
    display_name = "Pot Shuffle"


class Palette(Choice):
    option_default = 0
    option_good = 1
    option_blackout = 2
    option_puke = 3
    option_classic = 4
    option_grayscale = 5
    option_negative = 6
    option_dizzy = 7
    option_sick = 8


class OWPalette(Palette):
    """The type of palette shuffle to use for the overworld"""
    display_name = "Overworld Palette"


class UWPalette(Palette):
    """The type of palette shuffle to use for the underworld (caves, dungeons, etc.)"""
    display_name = "Underworld Palette"


class HUDPalette(Palette):
    """The type of palette shuffle to use for the HUD"""
    display_name = "Menu Palette"


class SwordPalette(Palette):
    """The type of palette shuffle to use for the sword"""
    display_name = "Sword Palette"


class ShieldPalette(Palette):
    """The type of palette shuffle to use for the shield"""
    display_name = "Shield Palette"


# class LinkPalette(Palette):
#     display_name = "Link Palette"


class HeartBeep(Choice):
    """How quickly the heart beep sound effect will play"""
    display_name = "Heart Beep Rate"
    option_normal = 0
    option_double = 1
    option_half = 2
    option_quarter = 3
    option_off = 4


class HeartColor(Choice):
    """The color of hearts in the HUD"""
    display_name = "Heart Color"
    option_red = 0
    option_blue = 1
    option_green = 2
    option_yellow = 3


class QuickSwap(DefaultOnToggle):
    """Allows you to quickly swap items while playing with L/R"""
    display_name = "L/R Quickswapping"


class MenuSpeed(Choice):
    """How quickly the menu appears/disappears"""
    display_name = "Menu Speed"
    option_normal = 0
    option_instant = 1,
    option_double = 2
    option_triple = 3
    option_quadruple = 4
    option_half = 5


class Music(DefaultOnToggle):
    """Whether background music will play in game"""
    display_name = "Play music"


class ReduceFlashing(DefaultOnToggle):
    """Reduces flashing for certain scenes such as the Misery Mire and Ganon's Tower opening cutscenes"""
    display_name = "Reduce Screen Flashes"


class TriforceHud(Choice):
    """When and how the triforce hunt HUD should display"""
    display_name = "Display Method for Triforce Hunt"
    option_normal = 0
    option_hide_goal = 1
    option_hide_required = 2
    option_hide_both = 3


class GlitchBoots(DefaultOnToggle):
    """If this is enabled, the player will start with Pegasus Boots when playing with overworld glitches or harder logic."""
    display_name = "Glitched Starting Boots"


class BeemizerRange(Range):
    value: int
    range_start = 0
    range_end = 100


class BeemizerTotalChance(BeemizerRange):
    """Percentage chance for each junk-fill item (rupees, bombs, arrows) to be
    replaced with either a bee swarm trap or a single bottle-filling bee."""
    default = 0
    display_name = "Beemizer Total Chance"


class BeemizerTrapChance(BeemizerRange):
    """Percentage chance for each replaced junk-fill item to be a bee swarm
    trap; all other replaced items are single bottle-filling bees."""
    default = 60
    display_name = "Beemizer Trap Chance"

class EnemyHealth(Choice):
    option_default = -1
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3
    default = option_default

    @property
    def enemizer_arg_value(self):
        return max(0, self.value)


class EnemyDamage(Choice):
    option_default = 0
    option_shuffled = 1
    option_chaos = 2
    # TODO: this doesn't work at all, do we need it?
    # alias_random = option_chaos # This was slated to be "removed", is this still the case?
    

class AllowCollect(Toggle):
    """Allows for !collect / co-op to auto-open chests containing items for other players.
    Off by default, because it currently crashes on real hardware."""
    display_name = "Allow Collection of checks for other players"


alttp_options: typing.Dict[str, type(Option)] = {
    "crystals_needed_for_gt": CrystalsTower,
    "crystals_needed_for_ganon": CrystalsGanon,
    "open_pyramid": OpenPyramid,
    "bigkey_shuffle": bigkey_shuffle,
    "smallkey_shuffle": smallkey_shuffle,
    "compass_shuffle": compass_shuffle,
    "map_shuffle": map_shuffle,
    "progressive": Progressive,
    "swordless": Swordless,
    "retro_bow": RetroBow,
    "retro_caves": RetroCaves,
    "hints": Hints,
    "scams": Scams,
    "restrict_dungeon_item_on_boss": RestrictBossItem,
    "boss_shuffle": LTTPBosses,
    "pot_shuffle": PotShuffle,
    "enemy_shuffle": EnemyShuffle,
    "killable_thieves": KillableThieves,
    "bush_shuffle": BushShuffle,
    "shop_item_slots": ShopItemSlots,
    "shop_price_modifier": ShopPriceModifier,
    "tile_shuffle": TileShuffle,
    "ow_palettes": OWPalette,
    "uw_palettes": UWPalette,
    "hud_palettes": HUDPalette,
    "sword_palettes": SwordPalette,
    "shield_palettes": ShieldPalette,
    # "link_palettes": LinkPalette,
    "heartbeep": HeartBeep,
    "heartcolor": HeartColor,
    "quickswap": QuickSwap,
    "menuspeed": MenuSpeed,
    "music": Music,
    "reduceflashing": ReduceFlashing,
    "triforcehud": TriforceHud,
    "glitch_boots": GlitchBoots,
    "beemizer_total_chance": BeemizerTotalChance,
    "beemizer_trap_chance": BeemizerTrapChance,
    "death_link": DeathLink,
    "allow_collect": AllowCollect,
    "start_inventory_from_pool": StartInventoryPool,
    "goal": Goal,
    "logic": Logic,
    "dungeon_counters": DungeonCounters,
    "sprite": Sprite,
    "mode": Mode,
    "timer": Timer,
    "triforce_pieces_mode": TriforcePiecesMode,
    "triforce_pieces_percentage": TriforcePiecesPercentage,
    "triforce_pieces_available": TriforcePiecesAvailable,
    "triforce_pieces_required": TriforcePiecesRequired,
    "triforce_pieces_extra": TriforcePiecesExtra,
    "difficulty": Difficulty,
    "item_functionality": ItemFunctionality,
    "countdown_start_time": CountdownStartTime,
    "red_clock_time": RedClockTime,
    "blue_clock_time": BlueClockTime,
    "green_clock_time": GreenClockTime,
    "entrance_shuffle": EntranceShuffle,
    "enemy_health": EnemyHealth,
    "enemy_damage": EnemyDamage,
    # required_medallions??
    # shuffle_prizes sprite_pool dark_room_logic shop_shuffle

}

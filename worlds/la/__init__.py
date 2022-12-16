# world/mygame/__init__.py

from .Options import links_awakening_options  # the options we defined earlier
from .Items import LinksAwakeningItem, item_list  # data used below to add items to the World
from .Locations import generate_reference_locations
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, RegionType, ItemClassification
from Utils import get_options, output_path
from .Common import *

class LinksAwakeningLocation(Location):  # or from Locations import MyGameLocation
    game = LINKS_AWAKENING  # name of the game/world this location is in

BASE_ID = 10000000

class LinksAwakeningWorld(World):
    """Insert description of the world/game here."""
    game: str = LINKS_AWAKENING # name of the game/world
    option_definitions = links_awakening_options  # options the player can set
    topology_present: bool = True  # show path to required location checks in spoiler

    # data_version is used to signal that items, locations or their names
    # changed. Set this to 0 during development so other games' clients do not
    # cache any texts, then increase by 1 for each release that makes changes.
    data_version = 0

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a propery.
    base_id = BASE_ID
    # Instead of dynamic numbering, IDs could be part of data.

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {
        item.item_name : BASE_ID + item.item_id for item in item_list
    }#{name: id for
                      # id, name in enumerate(links_awakening_items, base_id)}

    reference_locations = generate_reference_locations()
    location_name_to_id = {}
    #location_name_to_id = {name: id for
    #                       id, name in enumerate(mygame_locations, base_id)}

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    #item_name_groups = {
    #    "weapons": {"sword", "lance"}
    #}

    
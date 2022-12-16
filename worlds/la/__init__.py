# world/mygame/__init__.py

from .Options import links_awakening_options  # the options we defined earlier
from .Items import LinksAwakeningItem, links_awakening_items, ItemName, item_frequences # data used below to add items to the World
from .Locations import get_locations_to_id, create_regions_from_ladxr, LinksAwakeningLocation
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, RegionType, ItemClassification
from Utils import get_options, output_path
from .Common import *
#from worlds.generic.Rules import add_rule, set_rule, forbid_item

class LinksAwakeningWorld(World):
    """Insert description of the world/game here."""
    game: str = LINKS_AWAKENING # name of the game/world
    option_definitions = links_awakening_options  # options the player can set
    topology_present = True  # show path to required location checks in spoiler

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
        item.item_name : BASE_ID + item.item_id for item in links_awakening_items
    }

    item_name_to_data = {
        item.item_name : item for item in links_awakening_items
    }

    location_name_to_id = get_locations_to_id()

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    #item_name_groups = {
    #    "weapons": {"sword", "lance"}
    #}

    def create_item(self, item: str) -> LinksAwakeningItem:
        assert(False)

    def generate_output(self, output_directory: str):
        # assert(False)
        pass


    def create_regions(self) -> None:
        # Add regions to the multiworld. "Menu" is the required starting point.
        # Arguments to Region() are name, type, human_readable_name, player, world

        
        self.multiworld.regions = create_regions_from_ladxr(self.player, self.multiworld)

        for region in self.multiworld.regions:
            if region.name == "Start House":
                start = region
                break

        assert(start)

        r = Region("Menu", RegionType.Generic, "Menu", self.player, self.multiworld)        
        r.exits = [Entrance(self.player, "Start Game", r)]
        r.exits[0].connect(start)
        print()
        print(r.exits)
        print(start.exits)
        print()
        self.multiworld.regions.append(r)  # or use += [r...]

        
    def create_item(self, item_name: str):
        # This is called when AP wants to create an item by name (for plando) or
        # when you call it from your own code.
        item_data = self.item_name_to_data[item_name]

        classification = ItemClassification.progression if item_data.progression else ItemClassification.filler
        return LinksAwakeningItem(item_name, classification, item_data.item_id,
                        self.player)

    def create_event(self, event: str):
        # while we are at it, we can also add a helper to create events
        return LinksAwakeningItem(event, True, None, self.player)

    def create_items(self) -> None:    
        exclude = [item for item in self.multiworld.precollected_items[self.player]]

        for item in map(self.create_item, self.item_name_to_id):
            if item in exclude:
                exclude.remove(item)  # this is destructive. create unique list above
                self.multiworld.itempool.append(self.create_item("nothing"))
            else:
                for i in range(item_frequences.get(item, 1)):
                    self.multiworld.itempool.append(item)

        # itempool and number of locations should match up.
        # If this is not the case we want to fill the itempool with junk.
        junk = 106  # calculate this based on player settings
        self.multiworld.itempool += [self.create_item(ItemName.RUPEES_20) for _ in range(junk)]


def generate_basic(self) -> None:
    # place "Victory" at "Final Boss" and set collection as win condition
    self.multiworld.get_location("Windfish", self.player).place_locked_item(self.create_event("An Alarm Clock"))
    self.multiworld.completion_condition[self.player] = lambda state: state.has("An Alarm Clock", self.player)
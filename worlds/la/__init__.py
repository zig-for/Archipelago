# world/mygame/__init__.py

from .LADXR.locations.keyLocation import KeyLocation as LAXDRKeyLocation
from .Options import links_awakening_options  # the options we defined earlier
from .Items import LinksAwakeningItem, DungeonItemData, DungeonItemType, links_awakening_items, ItemName, ladxr_item_to_la_item_name, links_awakening_items_by_name # data used below to add items to the World
from .Locations import get_locations_to_id, create_regions_from_ladxr, LinksAwakeningLocation, links_awakening_dungeon_names, LinksAwakeningRegion
from worlds.AutoWorld import World
from BaseClasses import Location, Entrance, Item, RegionType, ItemClassification
from Utils import get_options, output_path
from .Common import *
from Fill import fill_restrictive
import os
from .LADXR.rom import ROM
from .LADXR.logic import Logic as LAXDRLogic
from .LADXR.settings import Settings as LADXRSettings
from .LADXR.worldSetup import WorldSetup as LADXRWorldSetup
from .LADXR.itempool import ItemPool as LADXRItemPool

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

    item_name_to_data = links_awakening_items_by_name

    location_name_to_id = get_locations_to_id()

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    #item_name_groups = {
    #    "weapons": {"sword", "lance"}
    #}

    prefill_dungeon_items = [[] for _ in range(9)]



    def create_item(self, item: str) -> LinksAwakeningItem:
        assert(False)

    def generate_output(self, output_directory: str):
        # assert(False)
        pass

    def generate_default_ladxr_logic(self):
        self.laxdr_options =  LADXRSettings()
        world_setup = LADXRWorldSetup()
        import random
        rnd = random.Random()
        world_setup.randomize(self.laxdr_options, rnd)
        self.ladxr_logic = LAXDRLogic(configuration_options=self.laxdr_options, world_setup=world_setup)
        self.ladxr_itempool = LADXRItemPool(self.ladxr_logic, self.laxdr_options, rnd).toDict()

    def create_regions(self) -> None:
        # Add regions to the multiworld. "Menu" is the required starting point.
        # Arguments to Region() are name, type, human_readable_name, player, world

        self.generate_default_ladxr_logic()
        self.multiworld.regions = create_regions_from_ladxr(self.player, self.multiworld, self.ladxr_logic)


        for region in self.multiworld.regions:
            if region.name == "Start House":
                start = region
                break

        assert(start)

        r = LinksAwakeningRegion("Menu", None, "Menu", self.player, self.multiworld)        
        r.exits = [Entrance(self.player, "Start Game", r)]
        r.exits[0].connect(start)
        
        self.multiworld.regions.append(r)  # or use += [r...]
        for r in self.multiworld.regions:
            for loc in r.locations:
                if isinstance(loc.ladxr_item, LAXDRKeyLocation):
                    #print(loc.ladxr_item.OPTIONS[0])
                    loc.place_locked_item(self.create_event(loc.ladxr_item.OPTIONS[0]))
        
    def create_item(self, item_name: str):
        # This is called when AP wants to create an item by name (for plando) or
        # when you call it from your own code.
        item_data = self.item_name_to_data[item_name]

        return LinksAwakeningItem(item_data, self.player)

    def create_event(self, event: str):
        # while we are at it, we can also add a helper to create events
        return Item(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:    
        exclude = [item for item in self.multiworld.precollected_items[self.player]]


        for ladx_item_name, count in self.ladxr_itempool.items():
            # event
            if ladx_item_name not in ladxr_item_to_la_item_name:
                continue
            item_name = ladxr_item_to_la_item_name[ladx_item_name]
            for _ in range(count):
                if item_name in exclude:
                    exclude.remove(item_name)  # this is destructive. create unique list above
                    self.multiworld.itempool.append(self.create_item("nothing"))
                else:
                    item = self.create_item(item_name)

                    # TODO: For now, lock instruments, don't do key shuffle
                    if isinstance(item.item_data, DungeonItemData):
                        if item.item_data.dungeon_item_type == DungeonItemType.INSTRUMENT:
                            search_string = f"INSTRUMENT{item.item_data.dungeon_index}"
                            # Find instrument, lock
                            # TODO: we should be able to pinpoint the region we want, save a lookup table please
                            found = False
                            for r in self.multiworld.regions:
                                for loc in r.locations:
                                    if len(loc.ladxr_item.OPTIONS) == 1 and loc.ladxr_item.OPTIONS[0] == search_string:
                                        loc.place_locked_item(item)
                                        found = True

                                if found:
                                    break
                            if found:
                                continue
                                        
                        else:
                            self.prefill_dungeon_items[item.item_data.dungeon_index - 1].append(item)
                        continue

                    self.multiworld.itempool.append(item)

                    


    def pre_fill(self):
        dungeon_locations = [[] for _ in range(9)]
        
        for r in self.multiworld.regions:
            if r.dungeon:
                dungeon_locations[r.dungeon-1] += r.locations
        
        all_state = self.multiworld.get_all_state(use_cache=True)

        for i, dungeon_items in enumerate(self.prefill_dungeon_items):
            dungeon_items =sorted(dungeon_items,key=lambda item: item.item_data.dungeon_item_type)
            fill_restrictive(self.multiworld, all_state, dungeon_locations[i], dungeon_items, single_player_placement=True, lock=True)
            
    def post_fill(self):
        # copy items back to locations
        for r in self.multiworld.regions:
            for loc in r.locations:
                #loc.item.ladxr_item.item = loc.
                if isinstance(loc, LinksAwakeningLocation):
                    if isinstance(loc.item, LinksAwakeningItem):
                        print(loc.item.item_data.ladxr_id)
                        loc.ladxr_item.item = loc.item.item_data.ladxr_id
    def generate_basic(self) -> None:
        # place "Victory" at "Final Boss" and set collection as win condition
        #self.multiworld.get_region("Wildfish", self.player).add
        
        windfish = self.multiworld.get_region("Windfish", self.player)
        l = Location(self.player, "Windfish", parent=windfish)
        windfish.locations = [l]
                #self.multiworld.get_region("Wildfish", self.player).add
        l.place_locked_item(self.create_event("An Alarm Clock"))
        
        self.multiworld.completion_condition[self.player] = lambda state: state.has("An Alarm Clock", player=self.player)





    def generate_output(self, output_directory: str):
        # How to generate the mod or ROM highly depends on the game
        # if the mod is written in Lua, Jinja can be used to fill a template
        # if the mod reads a json file, `json.dump()` can be used to generate that
        # code below is a dummy
        
        # point to a ROM specified by the installation
        #src = Utils.get_options()["mygame_options"]["rom_file"]
        # or point to worlds/mygame/data/mod_template
        #src = os.path.join(os.path.dirname(__file__), "data", "mod_template")
        # generate output path

        rom_path = "Legend of Zelda, The - Link's Awakening DX (USA, Europe) (SGB Enhanced).gbc"
        out_name = f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.player_name[self.player]}.gbc"
        out_file = os.path.join(output_directory, out_name)

        #out_file = os.path.join("D:\\dev\\Archipelago", out_name)
        out_file = out_name
        print(out_file)
        from .LADXR import generator 

        from .LADXR.main import get_parser
        parser = get_parser()
        args = parser.parse_args([rom_path, "-o", out_file, "--dump"])

        seed = 1
        import random
        
        

        rom = generator.generateRom(args, self.laxdr_options, bytes.fromhex(self.multiworld.seed_name), self.ladxr_logic, rnd=random.Random())
      
        handle = open(out_file, "wb")
        rom.save(handle, name="LADXR")
        handle.close()
        
# world/mygame/__init__.py

from .LADXR.locations.keyLocation import KeyLocation as LAXDRKeyLocation
from .LADXR.locations.tradeSequence import TradeSequenceItem
from .Options import links_awakening_options  # the options we defined earlier
from .Items import LinksAwakeningItem, DungeonItemData, DungeonItemType, links_awakening_items, ItemName, ladxr_item_to_la_item_name, links_awakening_items_by_name # data used below to add items to the World
from .Locations import get_locations_to_id, create_regions_from_ladxr, LinksAwakeningLocation, links_awakening_dungeon_names, LinksAwakeningRegion, prefilled_events
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
from Utils import get_options
import binascii
from .Rom import LADXDeltaPatch
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

    prefill_dungeon_items = None



    def create_item(self, item: str) -> LinksAwakeningItem:
        assert(False)

    def generate_output(self, output_directory: str):
        # assert(False)
        pass

    def generate_default_ladxr_logic(self):
        options = {
            option: getattr(self.multiworld, option)[self.player] for option in self.option_definitions
        }
        self.laxdr_options = LADXRSettings()
        for option in options.values():
            name, value = option.to_ladxr_option(options)
            if value == "true":
                value = 1
            elif value == "false":
                value = 0
                
            if name:
                self.laxdr_options.set( f"{name}={value}")
        self.laxdr_options.validate()
        world_setup = LADXRWorldSetup()
        world_setup.randomize(self.laxdr_options, self.multiworld.random)
        self.ladxr_logic = LAXDRLogic(configuration_options=self.laxdr_options, world_setup=world_setup)
        self.ladxr_itempool = LADXRItemPool(self.ladxr_logic, self.laxdr_options, self.multiworld.random).toDict()


    def create_regions(self) -> None:
        # Add regions to the multiworld. "Menu" is the required starting point.
        # Arguments to Region() are name, type, human_readable_name, player, world
        self.generate_default_ladxr_logic()

        regions = create_regions_from_ladxr(self.player, self.multiworld, self.ladxr_logic)
        self.multiworld.regions += regions

        start = None
        for region in regions:
            if region.name == "Start House":
                start = region
                break

        assert(start)

        r = LinksAwakeningRegion("Menu", None, "Menu", self.player, self.multiworld)        
        r.exits = [Entrance(self.player, "Start Game", r)]
        r.exits[0].connect(start)
        
        self.multiworld.regions.append(r)

        for region in regions:
            for loc in region.locations:
                if loc.event:
                    loc.place_locked_item(self.create_event(loc.ladxr_item.OPTIONS[0]))
        
        windfish = self.multiworld.get_region("Windfish", self.player)
        l = Location(self.player, "Windfish", parent=windfish)
        windfish.locations = [l]
                
        l.place_locked_item(self.create_event("An Alarm Clock"))
        
        self.multiworld.completion_condition[self.player] = lambda state: state.has("An Alarm Clock", player=self.player)

    def create_item(self, item_name: str):
        # This is called when AP wants to create an item by name (for plando) or
        # when you call it from your own code.
        item_data = self.item_name_to_data[item_name]

        return LinksAwakeningItem(item_data, self, self.player)

    def create_event(self, event: str):
        # while we are at it, we can also add a helper to create events
        return Item(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:    
        exclude = [item for item in self.multiworld.precollected_items[self.player]]
        self.prefill_dungeon_items = []
        self.trade_items = []
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

                    if not self.multiworld.tradequest[self.player] and ladx_item_name.startswith("TRADING_"):
                        self.trade_items.append(item)
                        continue
                    if isinstance(item.item_data, DungeonItemData):
                        if item.item_data.dungeon_item_type == DungeonItemType.INSTRUMENT:
                            search_string = f"INSTRUMENT{item.item_data.dungeon_index}"
                            # Find instrument, lock
                            # TODO: we should be able to pinpoint the region we want, save a lookup table please
                            found = False
                            for r in self.multiworld.get_regions():
                                if r.player != self.player:
                                    continue

                                for loc in r.locations:
                                    if not isinstance(loc, LinksAwakeningLocation):
                                        continue
                                    if len(loc.ladxr_item.OPTIONS) == 1 and loc.ladxr_item.OPTIONS[0] == search_string:
                                        loc.place_locked_item(item)
                                        found = True
                                if found:
                                    break                            
                        else:
                            self.prefill_dungeon_items.append(item)
                        continue

                    self.multiworld.itempool.append(item)

    def pre_fill(self):
        from BaseClasses import CollectionState
        dungeon_locations = []
        local_only_locations = []
        all_state = self.multiworld.get_all_state(use_cache=False)
        
        trendy_region = self.multiworld.get_region("Trendy Shop", self.player)
        event_location = Location(self.player, "Can Play Trendy Game", parent=trendy_region)
        trendy_region.locations.insert(0, event_location)
        event_location.place_locked_item(self.create_event("Can Play Trendy Game"))
        
        # For now, special case first item
        FORCE_START_ITEM = True
        if FORCE_START_ITEM:
            start_loc = self.multiworld.get_location("Tarin's Gift (Mabe Village)", self.player)
            possible_start_items = [item for item in self.multiworld.itempool 
                if item.player == self.player 
                    and item.item_data.ladxr_id in start_loc.ladxr_item.OPTIONS]
            
            start_item = self.multiworld.random.choice(possible_start_items)
            self.multiworld.itempool.remove(start_item)
            start_loc.place_locked_item(start_item)
        
        for r in self.multiworld.get_regions():
            if r.player != self.player:
                continue
            if r.dungeon_index:
                dungeon_locations += r.locations
                for location in r.locations:
                    if location.name == "Pit Button Chest (Tail Cave)":
                        # Don't place dungeon items on pit button chest, to reduce chance of the filler blowing up
                        dungeon_locations.remove(location)
                    location.dungeon = r.dungeon_index
                    orig_rule = location.item_rule
                    location.item_rule = lambda item, orig_rule=orig_rule: \
                        (not isinstance(item, DungeonItemData) or item.dungeon_index == location.dungeon) and orig_rule(item)

            for loc in r.locations:
                if not self.multiworld.tradequest[self.player] and isinstance(loc, LinksAwakeningLocation) and isinstance(loc.ladxr_item, TradeSequenceItem):
                    item = next(i for i in self.trade_items if i.item_data.ladxr_id == loc.ladxr_item.default_item)
                    loc.place_locked_item(item)                   
                elif isinstance(loc, LinksAwakeningLocation) and not loc.ladxr_item.MULTIWORLD and not loc.item:
                    local_only_locations.append(loc)

        dungeon_items = sorted(self.prefill_dungeon_items, key=lambda item: item.item_data.dungeon_item_type)
        self.multiworld.random.shuffle(dungeon_locations)
        fill_restrictive(self.multiworld, all_state, dungeon_locations, dungeon_items, lock=True)
        
        DO_EARLY_FILL = False
        if DO_EARLY_FILL:
            # Fill local only first
            # Double check that we haven't filled the location first so we don't double fill
            local_only_locations = [loc for loc in local_only_locations if not loc.item]
            self.multiworld.random.shuffle(local_only_locations)

            # Shuffle the pool first
            # extra disabled to suss out self locking trade items
            # self.multiworld.random.shuffle(self.multiworld.itempool)
            fill_restrictive(self.multiworld, all_state, local_only_locations, self.multiworld.itempool, lock=False, single_player_placement=True)
    def post_fill(self):

        #print("post_fill")
        pass

    name_cache = {}

    def guess_icon_for_other_world(self, other):
        if not self.name_cache:
            from .LADXR.locations.faceKey import FaceKey
            sample_key = FaceKey()
            forbidden = [
                "TRADING",
                "ITEM",
                "BAD",
                "SINGLE",
                "UPGRADE",
            ]
            for item in sample_key.OPTIONS:
                self.name_cache[item] = item
                splits = item.split("_")
                self.name_cache["".join(splits)] = item
                if 'RUPEES' in splits:
                    self.name_cache["".join(reversed(splits))] = item
                    
                for word in item.split("_"):
                    if word not in forbidden and not word.isnumeric():
                        self.name_cache[word] = item
            others = {
                'KEY': 'KEY',
                'COMPASS': 'COMPASS',
                'BIGKEY': 'NIGHTMARE_KEY',
                'MAP': 'MAP',
                'FLUTE': 'OCARINA',
                'SONG': 'OCARINA',
                'MUSHROOM': 'TOADSTOOL',
                'GLOVE': 'POWER_BRACELET',
                'BOOT': 'PEGASUS_BOOTS',
                'SHOE': 'PEGASUS_BOOTS',
                'SHOES': 'PEGASUS_BOOTS',
                'SANCTUARYHEARTCONTAINER': 'HEART_CONTAINER',
                'BOSSHEARTCONTAINER': 'HEART_CONTAINER',
                'HEARTCONTAINER': 'HEART_CONTAINER',
                'BOMBS': 'BOMB',
                # TODO: instruments because we can
            }
            self.name_cache |= others
            
        
        uppered = other.upper()
        if "BIG KEY" in uppered:
            return self.name_cache['BIGKEY']
        possibles = other.upper().split(" ")
        rejoined = "".join(possibles)
        if rejoined in self.name_cache:
            return self.name_cache[rejoined]
        for name in possibles:
            if name in self.name_cache:
                return self.name_cache[name]
        
        return "TRADING_ITEM_LETTER"




    def generate_output(self, output_directory: str):
        # copy items back to locations
        for r in self.multiworld.get_regions(self.player):
            for loc in r.locations:
                if isinstance(loc, LinksAwakeningLocation):
                    assert(loc.item)
                    # If we're a links awakening item, just use the item
                    if isinstance(loc.item, LinksAwakeningItem):
                        loc.ladxr_item.item = loc.item.item_data.ladxr_id

                    # TODO: if the item name contains "sword", use a sword icon, etc
                    # Otherwise, use a cute letter as the icon
                    else:
                        loc.ladxr_item.item = self.guess_icon_for_other_world(loc.item.name)
                        loc.ladxr_item.custom_item_name = loc.item.name

                    if loc.item:
                        loc.ladxr_item.item_owner = loc.item.player
                    else:
                        loc.ladxr_item.item_owner = self.player

                    # Kind of kludge, make it possible for the location to differentiate between local and remote items
                    loc.ladxr_item.location_owner = self.player

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

        rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.gbc")


        #out_file = os.path.join("D:\\dev\\Archipelago", out_name)
        out_file = out_name
        print(out_file)
        from .LADXR import generator 

        from .LADXR.main import get_parser
        parser = get_parser()
        args = parser.parse_args([rom_path, "-o", out_file, "--dump"])

        name_for_rom = self.multiworld.player_name[self.player]

        all_names = [self.multiworld.player_name[i + 1] for i in range(len(self.multiworld.player_name))]
        rom = generator.generateRom(
            args,
            self.laxdr_options,
            bytes.fromhex(self.multiworld.seed_name),
            self.ladxr_logic,
            rnd=self.multiworld.random,
            player_name=name_for_rom,
            player_names=all_names,
            player_id = self.player)
      
        handle = open(rompath, "wb")
        rom.save(handle, name="LADXR")
        handle.close()
        patch = LADXDeltaPatch(os.path.splitext(rompath)[0]+LADXDeltaPatch.patch_file_ending, player=self.player,
                                player_name=self.multiworld.player_name[self.player], patched_path=rompath)
        patch.write()
        # os.unlink(rompath)

    def generate_multi_key(self):
        return bytes.fromhex(self.multiworld.seed_name) + self.player.to_bytes(2, 'big')

    def modify_multidata(self, multidata: dict):
        multi_key = binascii.hexlify(self.generate_multi_key()).decode()
        multidata["connect_names"][multi_key] = multidata["connect_names"][self.multiworld.player_name[self.player]]

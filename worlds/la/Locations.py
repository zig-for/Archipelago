from BaseClasses import Region, RegionType, Entrance, Location

from .LADXR.logic import Logic as LAXDRLogic
from .LADXR.settings import Settings as LADXRSettings
from .LADXR.worldSetup import WorldSetup as LADXRWorldSetup
from .LADXR.logic.requirements import RequirementsSettings
from .LADXR.checkMetadata import checkMetadataTable
from .LADXR.locations.keyLocation import KeyLocation as LADXRKeyLocation
from .Common import *
from worlds.generic.Rules import add_rule, set_rule
from .Items import ladxr_item_to_la_item_name

class LinksAwakeningLocation(Location):  
    game = LINKS_AWAKENING

    def __init__(self, player: int, region, ladxr_item):
        name = ladxr_item.metadata.name
        self.event = isinstance(ladxr_item, LADXRKeyLocation)
        if self.event:
            # TODO: do translation to friendlier string
            name = ladxr_item.OPTIONS[0]
        super().__init__(player, ladxr_item.metadata.name)
        self.parent_region = region
        self.ladxr_item = ladxr_item


def translate_item_name(item):
    if item in ladxr_item_to_la_item_name:
        return ladxr_item_to_la_item_name[item]
    print(item)
    return item
         
#lambda name: ladxr_item_to_la_item_name[name]


class GameStateAdapater:
    def __init__(self, state, player):
        self.state = state
        self.player = player

    def __contains__(self, k):
        return self.state.has(k, self.player)

    def get(self, item, default):
        if item == "RUPEES":
            return 10000
        if item == "RUPEES_USED":
            return 0
        return self.state.prog_items.get((item, self.player), default)
    #def __getitem__(self, index):
    #    assert(False)

class LinksAwakeningEntrance(Entrance):
    def __init__(self, player: int, name, region, condition):
        super().__init__(player, name, region)
        if isinstance(condition, str):
            if condition in ladxr_item_to_la_item_name:
                # Test if in inventory
                self.condition = ladxr_item_to_la_item_name[condition]
            else:
                # Event
                self.condition = condition
        elif condition:
            # rewrite condition
            self.condition = condition.copyWithModifiedItemNames(translate_item_name)
        else:
            self.condition = None


    def access_rule(self, state):
        if isinstance(self.condition, str):
            return state.has(self.condition, self.player)
        if self.condition is None:
            return True
        return self.condition.test(GameStateAdapater(state, self.player))
        
def generate_default_ladxr_logic():
    options =  LADXRSettings()
    world_setup = LADXRWorldSetup()
    import random
    world_setup.randomize(options, random.Random())
    logic = LAXDRLogic(configuration_options=options, world_setup=world_setup)
    
    
    return logic

def walk_ladxdr(f, n, walked=set()):
    if n in walked:
        return
    f(n)
    walked.add(n)
    
    for o, req in n.simple_connections:
        walk_ladxdr(f, o, walked)
    for o, req in n.gated_connections:
        walk_ladxdr(f, o, walked)

def ladxr_region_to_name(n):
    name = n.name
    if not name:
        if len(n.items) == 1:
            name = str(n.items[0].metadata)
        elif n.dungeon:
            name = f"D{n.dungeon} Room"
        else:
            name = "No Name"

    return name

def create_regions_from_ladxr(player, multiworld):
    # No options, yet
    logic = generate_default_ladxr_logic()

    tmp = set()

    def print_items(n):
        print(f"Creating Region {ladxr_region_to_name(n)}")
        print("Has simple connections:")
        for region, info in n.simple_connections:    
            print("  " + ladxr_region_to_name(region) + " | " + str(info))
        print("Has gated connections:")

        for region, info in n.gated_connections:    
            print("  " + ladxr_region_to_name(region) + " | " + str(info))
        
        print("Has Locations:")
        for item in n.items:
            print("  " + str(item.metadata))
        print()

     
    used_names = {}

    regions = {}

    

    # Create regions
    for l in logic.location_list:
        # Temporarily uniqueify the name, until all regions are named
        name = ladxr_region_to_name(l)
        index = used_names.get(name, 0) + 1
        used_names[name] = index
        if index != 1:
            name += f" {index}"
        
        r = Region(name=name, type_=RegionType.Generic, hint="", player=player, world=multiworld)
        # TODO: if KeyLocation, add as Event instead
        r.locations = [LinksAwakeningLocation(player, r, i) for i in l.items]
        regions[l] = r


    # Create connections

    # 1. Loop over overworld overworld_entrance, generate connections, hook up inside/outside regions
    # 2. Loop over all regions - if haven't created connection between two regions, create, hookup two regions
    
    # for name, laxdr_entrance in logic.world.overworld_entrance.items():
    #     # TODO condition
    #     region = regions[laxdr_entrance.location]
    #     entrance = Entrance(player, name, region)
    #     region.exits.append(entrance)
    #     entrance.connect(regions[logic.world.indoor_location[name]])


    for ladxr_location in logic.location_list:
        for connection_location, connection_condition in ladxr_location.simple_connections + ladxr_location.gated_connections:
            region_a = regions[ladxr_location]
            region_b = regions[connection_location]
            # print(type(connection_condition))
            # This name ain't gonna work for entrance rando, we need to cross reference with logic.world.overworld_entrance
            entrance = LinksAwakeningEntrance(player, f"{region_a.name} -> {region_b.name}", region_a, connection_condition)
            region_a.exits.append(entrance)
            entrance.connect(region_b)
            pass
    return list(regions.values())


def get_locations_to_id():
    ret = {

    }

    # Magic to generate unique ids
    for s, v in checkMetadataTable.items():
        if s == "None":
            continue
        splits = s.split("-")
    
        
        main_id = int(splits[0], 16)
        sub_id = 0
        if len(splits) > 1:
            sub_id = splits[1]
            if sub_id.isnumeric():
                sub_id = int(sub_id)
            else:
                sub_id = 1
        name = str(v)
        ret[name] = main_id + sub_id

    return ret
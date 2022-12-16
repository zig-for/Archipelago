from BaseClasses import Region, RegionType, Entrance, Location

from .LADXR.logic import Logic as LAXDRLogic
from .LADXR.settings import Settings as LADXRSettings
from .LADXR.worldSetup import WorldSetup as LADXRWorldSetup
from .LADXR.logic.requirements import RequirementsSettings
from .LADXR.checkMetadata import checkMetadataTable
from .Common import *

class LinksAwakeningLocation(Location):  
    game = LINKS_AWAKENING
    def __init__(self, ladxr_item):
        self.ladxr_item = ladxr_item

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
        r.locations = [LinksAwakeningLocation(i for i in l.items)]
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
            # This ain't gonna work for entrance rando, we need to cross reference with logic.world.overworld_entrance
            entrance = Entrance(player, f"{region_a.name} -> {region_b.name}", region_a)
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
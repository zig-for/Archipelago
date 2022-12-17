from BaseClasses import Region, RegionType, Entrance, Location
from worlds.AutoWorld import LogicMixin



from .LADXR.logic.requirements import RequirementsSettings
from .LADXR.checkMetadata import checkMetadataTable
from .LADXR.locations.keyLocation import KeyLocation as LADXRKeyLocation
from .Common import *
from worlds.generic.Rules import add_rule, set_rule, add_item_rule
from .Items import ladxr_item_to_la_item_name, links_awakening_items, ItemName
from .LADXR.itempool import ItemPool as LADXRItemPool

links_awakening_dungeon_names = [
    "Tail Cave",
    "Bottle Grotto",
    "Key Cavern",
    "Angler's Tunnel",
    "Catfish's Maw",
    "Face Shrine",
    "Eagle's Tower",
    "Turtle Rock",
    "Color Dungeon"
]

def meta_to_name(meta):
    return f"{meta.name} ({meta.area})"
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
                sub_id = (int(sub_id) + 1) * 1000
            else:
                sub_id = 1000
        name = f"{v.name} ({v.area})"
        ret[name] = BASE_ID + main_id + sub_id

    return ret
locations_to_id = get_locations_to_id()
class LinksAwakeningLocation(Location):  
    game = LINKS_AWAKENING
    
    def __init__(self, player: int, region, ladxr_item):
        name = meta_to_name(ladxr_item.metadata)
        self.event = isinstance(ladxr_item, LADXRKeyLocation)
        if self.event:
            # TODO: do translation to friendlier string
            name = ladxr_item.OPTIONS[0]
        
        address = None
        if name not in ["ANGLER_KEYHOLE", "RAFT", "MEDICINE2", "CASTLE_BUTTON"]:
            address = locations_to_id[name]
        super().__init__(player, name, address)
        self.parent_region = region
        self.ladxr_item = ladxr_item
        def filter_item(item):
            #if item.player != player or item.item_data.ladxr_id in self.ladxr_item.OPTIONS:
            #   print(f"{self.name} = {item.name}")
            return item.player != player or item.item_data.ladxr_id in self.ladxr_item.OPTIONS
        add_item_rule(self, filter_item)

        
class LinksAwakeningLogic(LogicMixin):
    rupees = {
        ItemName.RUPEES_20: 20,
        ItemName.RUPEES_50: 50,
        ItemName.RUPEES_100: 100,
        ItemName.RUPEES_200: 200,
        ItemName.RUPEES_500: 500,
    }
    rupee_sinks = {
        "Fishing Game Heart Piece (Mabe Village)": 20,
        "Mamu (Ukuku Prairie)": 300,
        "Shop 200 Item (Mabe Village)": 200,
        "Shop 980 Item (Mabe Village)": 980,
    }
    def get_credits(self, player: int):
        return sum(self.count(item_name, player) * amount for item_name, amount in self.rupees.items())
    def get_debits(self, player: int):
        return sum(self.can_reach(location, player=player) * amount for location, amount in self.rupee_sinks.items())

    def has_rupees_to_spend(self, player: int, needed):
        credits = self.get_credits(player)
        debits = self.get_debits(player)
        
        return credits + needed <= debits
class LinksAwakeningRegion(Region):
    dungeon = None
    ladxr_region = None
    def __init__(self, name, ladxr_region, hint, player, world):
        super().__init__(name, RegionType.Generic, hint, player, world)
        if ladxr_region:
            self.ladxr_region = ladxr_region
            if ladxr_region.dungeon:
                self.dungeon = ladxr_region.dungeon
    





def translate_item_name(item):
    if item in ladxr_item_to_la_item_name:
        return ladxr_item_to_la_item_name[item]

    return item


class GameStateAdapater:
    def __init__(self, state, player):
        self.state = state
        self.player = player

    def __contains__(self, item):
        if item.endswith("_USED"):
            return False
        if item in ladxr_item_to_la_item_name:
            item = ladxr_item_to_la_item_name[item]
    
        return self.state.has(item, self.player)

    def get(self, item, default):
        # Hack - don't keep track of rupees for the moment
        if "ANGLER" in item:
            assert(False)
        if item == "RUPEES":
            return self.state.get_credits(self.player)
        elif item == "RUPEES_USED":
            return self.state.get_debits(self.player)
        elif item.endswith("_USED"):
            return 0
        else:
            item = ladxr_item_to_la_item_name[item]
        return self.state.prog_items.get((item, self.player), default)


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
            self.condition = condition #.copyWithModifiedItemNames(translate_item_name)
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
    rnd = random.Random()
    world_setup.randomize(options, rnd)
    logic = LAXDRLogic(configuration_options=options, world_setup=world_setup)
    itempool = LADXRItemPool(logic, options, rnd).toDict()
    return logic, itempool

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
            meta = n.items[0].metadata
            name = f"{meta.name} ({meta.area})"
        elif n.dungeon:
            name = f"D{n.dungeon} Room"
        else:
            name = "No Name"

    return name

def create_regions_from_ladxr(player, multiworld, logic):
    # No options, yet

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
        
        r = LinksAwakeningRegion(name=name, ladxr_region=l, hint="", player=player, world=multiworld)
        # TODO: if KeyLocation, add as Event instead
        # TODO: startlocation is too restrictive for multiworld
        r.locations = [LinksAwakeningLocation(player, r, i) for i in l.items]
        regions[l] = r


    for ladxr_location in logic.location_list:
        for connection_location, connection_condition in ladxr_location.simple_connections + ladxr_location.gated_connections:
            region_a = regions[ladxr_location]
            region_b = regions[connection_location]
            # TODO: This name ain't gonna work for entrance rando, we need to cross reference with logic.world.overworld_entrance
            entrance = LinksAwakeningEntrance(player, f"{region_a.name} -> {region_b.name}", region_a, connection_condition)
            region_a.exits.append(entrance)
            entrance.connect(region_b)

    

    return list(regions.values())



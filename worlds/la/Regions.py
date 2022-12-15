from BaseClasses import Region, MultiWorld, RegionType



def create_regions(world: MultiWorld, player: int) -> None:
    class OverworldRegion(Region):
        def __init__(self, name: str, hint: str = None):
            super().__init__(self, RegionType.Generic, "", player, world)
    
    class DungeonRegion(Region):
        def __init__(self, name: str, hint: str = None):
            super().__init__(self, RegionType.Dungeon, "", player, world)
    
    class InteriorRegion(Region):
        def __init__(self, name: str, hint: str = None):
            super().__init__(self, RegionType.Cave, "", player, world)
    
    dungeon1 = DungeonRegion('Dungeon 1')
    dungeon2 = DungeonRegion('Dungeon 2')
    dungeon3 = DungeonRegion('Dungeon 3')
    dungeon4 = DungeonRegion('Dungeon 4')
    dungeon5 = DungeonRegion('Dungeon 5')
    dungeon6 = DungeonRegion('Dungeon 6')
    dungeon7 = DungeonRegion('Dungeon 7')
    dungeon8 = DungeonRegion('Dungeon 8')
    dungeon9 = DungeonRegion('Dungeon 9')

    # Mabe Village
    mabe_village = OverworldRegion("Mabe Village")
    papahl_hoise = InteriorRegion("Papahl House")
    rooster_grave = InteriorRegion("Rooster Grave")
    madam_bowwow = InteriorRegion("Madam Bowwow")
    ulrira = InteriorRegion("Ulrira")
    mabe_phone = InteriorRegion("Mabe Phone")
    library = InteriorRegion("Library")
    trendy_shop = InteriorRegion("Trendy Shop")
    start_house = InteriorRegion("Start House") # hmmm
    dream_hut = InteriorRegion("Dream Hut")
    kennel = InteriorRegion("Kennel")

    # Sword Beach
    sword_beach = OverworldRegion("Sword Beach")
    banana_seller = InteriorRegion("Banana Seller")
    boomerang_cave = InteriorRegion("Boomerage Cave")
    ghost_house = InteriorRegion("Ghost House")

    # Forest
    forest = OverworldRegion("Forest")
    forest_heartpiece = OverworldRegion("Forest Heartpiece")
    # This is a check, not a Region
    # WITCH_HUT = InteriorRegion("Witch's Hut")
    crazy_tracy_hut_outside = OverworldRegion("Outside Crazy Tracy's Hut")
    crazy_tracy_hut = InteriorRegion("Crazy Tracy's Hut")
    forest_madbatter = InteriorRegion("Forest Madbatter")
    forest_cave = InteriorRegion("Forest Cave")
    forest_toadstool = InteriorRegion("Forest Toadstool")
    hookshot_cave = InteriorRegion("Hookshot Cave")

    # Swamp
    swamp = OverworldRegion("Swamp")
    outside_writes_house = OverworldRegion("Outside Write's House")
    writes_house = InteriorRegion("Write's House")
    writes_cave = InteriorRegion("Write's Cave")

    # Swamp
    graveyard = OverworldRegion("Graveyard")
    graveyard_photo = InteriorRegion("Graveyard Photo House")
    graveyard_cave = InteriorRegion("Graveyard Cave")
    moblin_cave = InteriorRegion("Moblin Cave")

    # Ukuku Prairie
    ukuku_prarie = OverworldRegion("Moblin Cave")
    ukuku_prarie_left_phone = InteriorRegion("Ukuku Left Phone")
    ukuku_prarie_right_phone = InteriorRegion("Ukuku Right Phone")
    ukuku_prarie_left_fairy = InteriorRegion("Ukuku Left Fairy")
    ukuku_prarie_left_cave_2 = InteriorRegion("Ukuku Left Cave 2")
    mamu = InteriorRegion("Mamu")
    prairie_island_seashell = OverworldRegion("Prarie_Island_Seashell")
    castle_jump_cave = InteriorRegion("Castle Jump Cave")

    
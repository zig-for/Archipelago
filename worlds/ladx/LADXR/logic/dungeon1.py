from .requirements import *
from .location import Location
from ..locations.all import *

from collections import defaultdict

from enum import Enum, IntEnum

class Direction(IntEnum):
    Right = 0
    Left = 1
    Up = 2
    Down = 3
    Stairs = 4


opposite_dir = {
    Direction.Stairs: Direction.Stairs,
    Direction.Right: Direction.Left,
    Direction.Left: Direction.Right,
    Direction.Up: Direction.Down,
    Direction.Down: Direction.Up,
}

# Used for centered doors
class DoorDir(Enum):
    LR = -1
    UD = -2
    LRUpOne = -3
    D1Rail = -4

TwoWideGapLR = 0b11100111
TwoWideGapUD = 0b111110011111
Impassable = 0b1111111111

class DoorType(Enum):
    Open = 0
    Shutter = 1
    Bomb = 2
    Key = 3
    NightmareKey = 4
    OneWay = 5
    OneWayBlocked = 6
    Stairs = 7
    Pit = 8
    Water = 9
    Lava = 10
    TwoDLadder = 11
    Drop = 12
    DropTarget = 13

skip_door_connect = {
    DoorType.OneWayBlocked,
    DoorType.DropTarget,
    DoorType.Lava,
    DoorType.Pit
}

from ..locations.itemInfo import ItemInfo
from typing import Union, Tuple, Any
from dataclasses import dataclass

class KillMiniboss:
    pass

class KillBoss:
    pass

# TODO: has_keyblock
@dataclass
class RoomLogic:
    start: Union[Direction, Tuple[Direction, Any], "RoomLogic", None]
    requirements: Any
    end: Union[Direction, Tuple[Direction, Any], "RoomLogic", ItemInfo, None]
    one_way: bool = False # do I even use this rn?


from typing import Set
@dataclass
class Exit:
    room: 'Room'
    door_type: DoorType
    direction: Direction
    mask: Optional[int]
    locked: bool = False
    other_exits: Set = None

class Room:
    def __init__(self, id, name, borders, logic = [], two_d = False):
        self.id = id
        self.borders = borders
        for border in self.borders:
            if isinstance(border, list):
                border.sort()
            else:
                border = [border]
        if len(self.borders) <= 4:
            self.borders.append(None)
        self.exits = []
        self.location = None
        self.logic = logic
        self.two_d = two_d
        self.name = name
        self.location = None

        for l in self.logic:
            if isinstance(l.start, Direction):
                l.start = (l.start, self.borders[l.start])
            if isinstance(l.end, Direction):
                l.end = (l.end, self.borders[l.end])
    def __repr__(self) -> str:
        return self.name
    def connect(self, other, direction, door, other_door = None, mask = None, locked = False):
        if direction != Direction.Stairs:
            our_border = self.borders[direction]
            opposite_border = other.borders[opposite_dir[direction]]
            if isinstance(our_border, DoorDir) or isinstance(opposite_border, DoorDir):
                assert our_border == opposite_border
            elif type(our_border) == type(opposite_border):
                assert our_border == opposite_border
            elif isinstance(our_border, list):
                assert opposite_border in our_border
            elif isinstance(opposite_border, list):
                assert our_border in opposite_border
            if not mask:
                assert not isinstance(our_border, list)
                mask = our_border
        self.exits.append(Exit(other, door, direction, mask, locked))
        
        if door == DoorType.OneWay:
            assert other_door and other_door == DoorType.OneWayBlocked
        if other_door == DoorType.OneWay:
            assert door and door == DoorType.OneWayBlocked

        # TODO: do we always want to do this?
        other.exits.append(Exit(self, other_door or door, opposite_dir[direction], mask))

    def add(self, locations):
        self.locations.append(locations)

    # Why doesn't this live on room?
    def location_for_dir_mask(self, mask, dir):
        if dir == Direction.Stairs:
            # TODO: really should just add stairs as an optional bit
            border = None
        else:
            border = self.borders[dir]
        if mask:
            assert mask == border or mask in border
            border = mask
        assert border == None or isinstance(border, int) or isinstance(border, DoorDir), border
        return self.exit_locations[(dir, border)] or self.location

class Dungeon:
    entrance_room: Room
    entrance: Location
    instrument: Room
    boss_room: Room

    def __init__(self, index):
        self.index = index

    def unlink_and_return_rooms(self):
        all_rooms = set()        
        self.walk_rooms(None, None, walked=all_rooms)

        for room in all_rooms:
            for exit in room.exits:
                if not exit.locked:
                    exit.room = None
        all_rooms = list(all_rooms)
        # Hmm
        # all_rooms.sort()
 
        return all_rooms

    @staticmethod
    def get_opposite_door_list(pool, exit):
        return pool[opposite_dir[exit.direction]][exit.mask]

    @staticmethod
    def remove_from_door_pool(door_pool, room, exit):        
        door_pool[exit.direction][exit.mask].remove((room, exit))

    # TODO: doesn't use self
    def fill_other_exits_for_exit(self, room, exit):
        # Find out where we can go
        # TODO: handle higher logic
        # TODO: handle chained logic
        # TODO: handle locked room pairs
        
        going_to = set()
        # TODO: this should be a set of exits
        # we need to re-associate dir->mask, maybe in logic
        # probably in logic, it will be more sane
        going_to.add((exit.direction, exit.mask))
        # why are we tracking seen things?
        seen_things = set()
        has_any_door_logic = False
        for logic in room.logic:
            if logic.start != None:
                has_any_door_logic = True
                break
        
        if has_any_door_logic:
            continue_loop = True
            while continue_loop:
                continue_loop = False
                for logic in room.logic:
                    if isinstance(logic.start, (tuple, type(None))) and isinstance(logic.end, (tuple, type(None))):
                        seen_things.add(logic.start)
                        seen_things.add(logic.end)

                        if logic.start in going_to and logic.end not in going_to:
                            going_to.add(logic.end)
                            continue_loop = True
                        elif logic.end in going_to and logic.start not in going_to and not logic.one_way:
                            going_to.add(logic.start)
                            continue_loop = True
        else:
            going_to = set()
            going_to.add(None)
            for other_exit in room.exits:
                seen_things.add((other_exit.direction, other_exit.mask))

        if None in going_to:
            going_to.remove(None)
            for other_exit in room.exits:
                going_to.add((other_exit.direction, other_exit.mask))

        #for dir, exit in going_to:
        #    assert not exit.locked
        assert going_to != None
        exit.other_exits = going_to

    
    def randomize(self, random, room_pool):
        # unseen_entrances = {
        #     Direction.Left: defaultdict(list),
        #     Direction.Right: defaultdict(list),
        #     Direction.Up: defaultdict(list),
        #     Direction.Down: defaultdict(list),
        #     Direction.Stairs: defaultdict(list),
        #     }
        unseen_exits = []
        # TODO: comprehension
        assert self.entrance_room in room_pool
        for room in room_pool:
            for exit in room.exits:
                self.fill_other_exits_for_exit(room, exit)
                unseen_exits.append((room, exit))
            if room is self.entrance_room:
                print(room.exits)
        seen_exits = {
            Direction.Left: defaultdict(list),
            Direction.Right: defaultdict(list),
            Direction.Up: defaultdict(list),
            Direction.Down: defaultdict(list),
            Direction.Stairs: defaultdict(list),
            }
        
        random.shuffle(unseen_exits)

        # TODO: assumes all exits are viable - is this true?
        for exit in self.entrance_room.exits:
            self.see_exit(self.entrance_room, exit, unseen_exits, seen_exits)

        while unseen_exits:
            # print(len(unseen_exits))
            connector_exits = [(room, exit) for room, exit in unseen_exits if len(exit.other_exits) > 1]
            # Hey this almost works! we sometimes hit this
            assert connector_exits
            random.shuffle(connector_exits) 

            # TODO: check if this is mathematically sound        
            for room, exit in connector_exits:
                # We have a room we haven't seen before, try to link with one we have
                print(f"Search for {room.name} {exit.direction} {exit.mask}")
                # TODO: split seen, unseen, pool
                pool = self.get_opposite_door_list(seen_exits, exit)
                unfiltered_pool = pool
                pool = [(room, exit_) for room, exit_ in pool if not exit_.room and len(exit_.other_exits) > 1]

                # Note: we can't allow closing off here
                # Need to separate unseen exits into things that are deadends and things that aren't
                if pool:
                    # Found it
                    other_room, other_exit = random.choice(pool)
                    pool.remove((other_room, other_exit))
                    exit.room = other_room
                    other_exit.room = room
                    assert exit != other_exit
                    print(f"chose {other_room.name} -> {room.name} {exit.direction} {exit.mask} ")

                    print(pool)
                    old_len = len(unseen_exits)
                    self.see_exit(room, exit, unseen_exits, seen_exits)
                    assert len(unseen_exits) != old_len
                    break
                else:
                    print(f"None found (unfiltered {len(unfiltered_pool)})")
            else:
                assert False, unseen_exits

                


    # Wrong.
    # For each existing entrance
    # Find a room we haven't seen yet that has a matching entrance
    # Pair them
    # Once we run out of entrances, pick every entrance
    # 
    # Need new dir type for drop/drop target? Maybe?
    # Need to make sure we handle one way entrances properly
    # Need to walk locked rooms when we add things


    # ahhhhhh how will this deal with one way and broken paths
    # this needs to do unseen entrances
    def see_exit(self, room, exit_to_see, unseen_exits, seen_exits):
        if (room, exit_to_see) in seen_exits[exit_to_see.direction][exit_to_see.mask]:
            return False

        going_to = exit_to_see.other_exits
        assert going_to, room.name
        new_exits = []

        for exit in room.exits:
            if (exit.direction, exit.mask) in going_to:
                if (room, exit) in unseen_exits:
                    seen_exits[exit.direction][exit.mask].append((room, exit))
                    unseen_exits.remove((room, exit))
                    new_exits.append(exit)

        # Handle any locked rooms
        for exit in new_exits:
            if exit.locked:
                self.see_exit(exit.room, exit, unseen_exits, seen_exits)        

        # self.remove_from_door_pool(unlinked_entrances, room, exit)

                #possibles = self.get_opposite_door_list(unlinked_entrances, exit)
        #         chosen_room, chosen_exit = random.choice(possibles)
        #         exit.room = chosen_room
        #         chosen_exit.room = room
        #         chosen_rooms.add(chosen_room)
        # for room in chosen_rooms:
        #     self.randomize_from_room(random, door_pool, room, walked)

    def finalize(self):
        def initialize_locations(room):
            room.location = Location(room.name, dungeon=self.index)
            room.exit_locations = {}
            # TODO staircase, etc
            for dir, border in enumerate(room.borders):
                room.exit_locations[Direction(dir)] = []
                if isinstance(border, list):
                    for sub_border in border:
                        room.exit_locations[(dir, sub_border)] = None
                else:
                    room.exit_locations[(dir, border)] = None
            room.exit_locations[(Direction.Stairs, None)] = None

            for logic in room.logic:
                req = logic.requirements
                if req == KillMiniboss:
                    req = self.miniboss_req
                elif req == KillBoss:
                    req = self.boss_req

                def get_loc_for_logic_endpoint(endpoint):
                    if endpoint:
                        if isinstance(endpoint, ItemInfo):
                            loc = Location(dungeon=self.index)
                            loc.add(endpoint)
                            return loc
                        elif isinstance(endpoint, Direction):
                            if endpoint == Direction.Stairs:
                                key = (endpoint, None)
                            else:
                                key = (endpoint, room.borders[endpoint])
                        elif isinstance(endpoint, tuple):
                            key = endpoint
                        else:
                            assert False, endpoint

                        if not room.exit_locations[key]:
                            room.exit_locations[key] = Location(f"{room.name} {endpoint}", dungeon=self.index)
                        return room.exit_locations[key]
                    else:
                        return room.location

                start = get_loc_for_logic_endpoint(logic.start)
                end = get_loc_for_logic_endpoint(logic.end)
                start.connect(end, req)

        self.walk_rooms(initialize_locations)

        def set_connections(room):
            for exit in room.exits:
                if exit.door_type not in skip_door_connect:
                    exit_location = room.location_for_dir_mask(exit.mask, dir)
                    enter_location = exit.room.location_for_dir_mask(exit.mask, opposite_dir[dir])
                    exit_location.connect(enter_location, req=None, one_way=True)

        self.walk_rooms(set_connections)

        def print_connection(room, dir, exit):
            print(f"{room.name} -> {exit.room.name}")

        self.walk_rooms(connection_cb=print_connection)

        self.entrance = self.entrance_room.location

    def walk_rooms(self, room_cb=None, connection_cb=None, room=None, walked=None):
        if walked is None:
            walked = set()
        if not room:
            room = self.entrance_room
        if room in walked:
            return
        walked.add(room)
        if room_cb:
            room_cb(room)
        for exit in room.exits:
            if connection_cb:
                connection_cb(room, dir, exit)
            self.walk_rooms(room_cb, connection_cb, room=exit.room, walked=walked)


class Dungeon1(Dungeon):
    def __init__(self, options, world_setup, r):
        super().__init__(1)
        
        # TODO: missing an item!

        self.miniboss_req = r.miniboss_requirements[world_setup.miniboss_mapping[0]]
        self.boss_req = r.boss_requirements[world_setup.boss_mapping[0]]

        entrance = Room(0x117, "Tail Key Foyer",  [Impassable, TwoWideGapLR, TwoWideGapUD, Impassable])
        self.entrance_room = entrance
        hard_hat_room = Room(0x116, "Hard Hats Room",       [TwoWideGapLR, DoorDir.LR, Impassable, Impassable], 
                             [RoomLogic(None, OR(BOMB, r.push_hardhat), DroppedKey(0x116))])
        entrance.connect(hard_hat_room, Direction.Left, DoorType.Open)
        pit_button_room = Room(0x113, "Pit Button Room", [TwoWideGapLR, DoorDir.LR, Impassable, TwoWideGapUD],
                               [RoomLogic(None, None, DungeonChest(0x113))])
        entrance.connect(pit_button_room, Direction.Up, DoorType.Open)

        keese_cracks_room = Room(0x112, "Keese Cracks Room", [DoorDir.LR, Impassable, DoorDir.UD, Impassable],
                               [RoomLogic(Direction.Up, r.attack_hookshot, Direction.Right)]) # Kill keese

        keese_cracks_room.connect(pit_button_room, Direction.Right, DoorType.Shutter, DoorType.Open)

        two_stalfos_room = Room(0x114, "Two Stalfos Two Keese Room", [Impassable, TwoWideGapLR, DoorDir.UD, Impassable], [RoomLogic(None, r.attack_hookshot, DungeonChest(0x114))])
        pit_button_room.connect(two_stalfos_room, Direction.Right, DoorType.Open)

        four_zol = Room(0x115, "D1 Four Zol Chest Room", [DoorDir.LR, Impassable, Impassable, Impassable], [RoomLogic(None, r.attack_hookshot, DungeonChest(0x115))])
            
        # Technically needs enemy kills to exit, but it's a deadend
        four_zol.connect(hard_hat_room, Direction.Right, DoorType.Shutter, DoorType.Open)
        
        # TODO: dupe room?
        block_room_up = Room(0x10F, "Tail Cave Block Room", [DoorDir.LR, 0b11011111, 0b1111111011, DoorDir.UD])
        block_room_down = Room(0x10F, "Tail Cave Block Room", [DoorDir.LR, 0b11110011, 0b1111111011, DoorDir.UD])

        two_stalfos_room.connect(block_room_down, Direction.Up, DoorType.OneWay, DoorType.OneWayBlocked)
        
        moldom_sparks_room = Room(0x10E, "Sparks and Moldorm Chest Room", [[0b11110011, 0b11011111], 0b11000001, 0b1100000001, Impassable],
                           [RoomLogic(None, None, DungeonChest(0x10D))])
        
        moldom_sparks_room.connect(block_room_up, Direction.Right, DoorType.Open, mask=0b11011111)
        moldom_sparks_room.connect(block_room_down, Direction.Right, DoorType.Open, mask=0b11110011)

        moldom_room = Room(0x10D, "Moldorm Chest Room", [0b11000001, 0b11101111, 0b1000000011, DoorDir.UD],
                           [RoomLogic(None, OR(r.attack_hookshot_powder, SHIELD), DungeonChest(0x10D))],
                           [RoomLogic(Direction.Down, SWORD, None)])
        
        moldom_room.connect(moldom_sparks_room, Direction.Right, DoorType.Open)
        keese_cracks_room.connect(moldom_room, Direction.Up, DoorType.Shutter, DoorType.Open)

        seashell_room = Room(0x10C, "Hidden Seashell Room", [0b11101111, Impassable, Impassable, Impassable],
                             [RoomLogic(None, None, DungeonChest(0x10C))])
        seashell_room.connect(moldom_room, Direction.Right, DoorType.Bomb)

        blade_block_room = Room(0x107, "Blade Block Room", [0b11111011, Impassable, DoorDir.UD, 0b1000000011])
        blade_block_room.connect(moldom_room, Direction.Down, DoorType.Open)

        blade_block_room_overlook = Room(0x107, "Blade Block Room Overlook", [0b00001111, Impassable, Impassable, Impassable])


        # Special rooms, pair together
        # TODO: split L into two parts for neater spoiler gen
        spark_block_push_room_l = Room(0x104, "Spark Block Push Room Left", [DoorDir.D1Rail,DoorDir.LRUpOne, Impassable, DoorDir.UD])
        spark_block_push_room_r = Room(0x105, "Spark Block Push Room Right", [Impassable, DoorDir.D1Rail, Impassable, Impassable])
        spark_block_push_room_l.connect(spark_block_push_room_r, Direction.Right, DoorType.Open)
        spark_block_push_room_l.connect(blade_block_room, Direction.Down, DoorType.Key)

        spike_room_before_feather = Room(0x103, "Spikes Before Feather Room", [DoorDir.LRUpOne, Impassable, Impassable, Impassable], 
                                         [RoomLogic(None, SHIELD, Direction.Stairs)])
        spike_room_before_feather.connect(spark_block_push_room_l, Direction.Right, DoorType.Open, DoorType.Shutter)

        underground_right = Room(0x109, "Under D1 Right", [Impassable, 0b10001111, Impassable, Impassable], two_d=True)
        underground_right.connect(spike_room_before_feather, Direction.Stairs, DoorType.Stairs)
        underground_left = Room(0x108, "Under D1 Left", [0b10001111, Impassable, Impassable, Impassable], two_d=True)
        underground_left.connect(underground_right, Direction.Right, DoorType.Open)

        feather_four_torches_room = Room(0x001, "Four Torches Room", [Impassable, Impassable, 0b1111011111, Impassable])
        feather_four_torches_room.connect(underground_left, Direction.Stairs, DoorType.Stairs)

        feather_hallway = Room(0x10C, "Feather Hallway", [Impassable, Impassable, 0b1111011111, 0b1111011111])
        feather_hallway.connect(feather_four_torches_room, Direction.Down, DoorType.Open)

        feather_chest = Room(0x11D, "Feather Chest", [Impassable, Impassable, Impassable, 0b1111011111], [RoomLogic(None, None, DungeonChest(0x11D))])
        feather_chest.connect(feather_hallway, Direction.Down, DoorType.Open)

        # TODO: keylogic!
        boss_key_right = Room(0x109, "D1 Nightmare Key Jump", [Impassable, 0b00001111, Impassable, 0b1111111011],
                              [RoomLogic(None, AND(FEATHER, KEY1), Direction.Left)])
        boss_key_right.connect(block_room_up, Direction.Down, DoorType.Open)
        boss_key = Room(0x108, "D1 Nightmare Key Chest", [0b00001111, 0b00001111, Impassable, Impassable],
                        [RoomLogic(None, None, DungeonChest(0x108))])

        boss_key.connect(blade_block_room_overlook, Direction.Left, DoorType.Open)
        boss_key.connect(boss_key_right, Direction.Right, DoorType.Open)
        
        boss_key_underlook = Room(0x108, "D1 Nightmare Key Underlook", [Impassable, 0b11111011, Impassable, 0b1100000001])
        boss_key_underlook.connect(blade_block_room, Direction.Left, DoorType.Pit)
        boss_key_underlook.connect(moldom_sparks_room, Direction.Down, DoorType.Open)
        
        spark_jump_room = Room(0x110, "Spark Jump Room", [DoorDir.LR, DoorDir.LR, TwoWideGapUD, Impassable],
                               [RoomLogic(None, FEATHER, Direction.Right)])
        spark_jump_room.connect(block_room_down, Direction.Left, DoorType.Key)

        three_kind = Room(0x10A, "D1 Three of a Kind Room", [Impassable, Impassable, Impassable, TwoWideGapUD],
                          [RoomLogic(None, r.attack_hookshot, DungeonChest(0x10A))])
        three_kind.connect(spark_jump_room, Direction.Down, DoorType.Open, DoorType.Open)

        miniboss = Room(0x111, "D1 Miniboss", [Impassable, DoorDir.LR, DoorDir.UD, Impassable],
                          [RoomLogic(Direction.Left, KillMiniboss, None)])
        miniboss.connect(spark_jump_room, Direction.Left, DoorType.Shutter, DoorType.Open)

        boss_foyer = Room(0x10B, "D1 Boss Foyer", [Impassable, Impassable, DoorDir.UD, DoorDir.UD])
        boss_foyer.connect(miniboss, Direction.Down, DoorType.Open, DoorType.Shutter)

        boss = Room(0x106, "D1 Boss", [Impassable, Impassable, DoorDir.UD, DoorDir.UD],
                    [RoomLogic(Direction.Down, KillBoss, None),
                    RoomLogic(None, None, HeartContainer(0x106)),
                    RoomLogic(Direction.Up, KillBoss, None)])
        boss.connect(boss_foyer, Direction.Down, DoorType.Shutter, DoorType.Open)

        fail_left = Room(0x11A, "D1 Fall Left", [0b00000001, Impassable, Impassable, Impassable], two_d=True)
        boss.connect(fail_left, Direction.Stairs, DoorType.Drop, DoorType.DropTarget, locked=True)
        fail_right = Room(0x11B, "D1 Fall Right", [Impassable, 0b00000001, Impassable, Impassable], two_d=True)
        fail_right.connect(fail_left, Direction.Left, DoorType.Open)
        fail_right.connect(boss_foyer, Direction.Stairs, DoorType.Stairs)

        instrument = Room(0x102, "D1 Instrument Room", [Impassable, Impassable, Impassable, DoorDir.UD], 
                          [RoomLogic(None, None, Instrument(0x102))])
        boss.connect(instrument, Direction.Up, DoorType.Shutter, DoorType.Open, locked=True)
        self.boss_room = boss


class NoDungeon1:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=1)
        Location(dungeon=1).add(HeartContainer(0x106), Instrument(0x102)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[0]])
        self.entrance = entrance

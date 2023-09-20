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
    Drop = 5
    DropTarget = 6

opposite_dir = {
    Direction.Drop: Direction.DropTarget,
    Direction.DropTarget: Direction.Drop,
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
    target: 'Room'
    door_type: DoorType
    direction: Direction
    mask: Optional[int]
    locked: bool = False
    parent: 'Room' = None
    other_exits: Set = None

    def __hash__(self) -> int:
        return hash((self.parent, self.door_type, self.direction, self.mask))

class Room:
    def __init__(self, id, name, borders, logic = [], two_d = False):
        self.room_id = id
        self.borders = borders
        for border in self.borders:
            if isinstance(border, list):
                border.sort()
            else:
                border = [border]
        if len(self.borders) < 7:
            self.borders.extend([None] * (7 - len(self.borders)))
        self.exits = []
        self.exits_by_dir_mask = {}
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

    def post_exits_added(self):
        for exit in self.exits:
            exit.parent = self
            self.exits_by_dir_mask[(exit.direction, exit.mask)] = exit

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
        if door == DoorType.Drop:
            assert other_door and other_door == DoorType.DropTarget
            assert locked

        # TODO: do we always want to do this?
        other.exits.append(Exit(self, other_door or door, opposite_dir[direction], mask, locked))

    def add(self, locations):
        self.locations.append(locations)

    # Why doesn't this live on room?
    def location_for_dir_mask(self, mask, dir):
        if dir >= Direction.Stairs:
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

    def __init__(self, dungeon_id):
        self.dungeon_id = dungeon_id

    def unlink_and_return_rooms(self):
        all_rooms = set()
        self.walk_rooms(None, None, walked=all_rooms)

        for room in all_rooms:
            room.post_exits_added()
        for room in all_rooms:
            for exit in room.exits:
                self.fill_other_exits_for_exit(exit)
        for room in all_rooms:
            for exit in room.exits:
                if not exit.locked:
                    exit.target = None
        
        all_rooms = list(all_rooms)
        # Hmm
        # all_rooms.sort()
 
        return all_rooms

    @staticmethod
    def get_opposite_door_list(pool, exit):
        return pool[opposite_dir[exit.direction]][exit.mask]

    @staticmethod
    def remove_from_door_pool(door_pool, exit):        
        door_pool[exit.direction][exit.mask].remove(exit)

    # TODO: doesn't use self
    def find_other_exits_for_exit(self, exit_to_search, other_exits, seen_exits = None):
        # Find out where we can go
        # TODO: handle higher logic
        # TODO: handle chained logic
        # TODO: handle locked room pairs

        # this is totally wrong lmao

        
        room = exit_to_search.parent

        if seen_exits == None:
            seen_exits = set()

        if exit_to_search in seen_exits:
            return
        seen_exits.add(exit_to_search)        
        # TODO: this should be a set of exits
        # we need to re-associate dir->mask, maybe in logic
        # probably in logic, it will be more sane
        # other_exits.add(exit)
        # why are we tracking seen things?
        has_any_door_logic = False
        for logic in room.logic:
            if logic.start != None:
                has_any_door_logic = True
                break

        locked_exits = set()

        if has_any_door_logic:
            logicked_exits = []
            for logic in room.logic:
                # TODO: translate the logic on room creation
                # TODO: translate whole room logic on room creation
                if isinstance(logic.start, (tuple, type(None))) and isinstance(logic.end, (tuple, type(None))):
                    start_exit = room.exits_by_dir_mask[logic.start] if logic.start else None
                    end_exit = room.exits_by_dir_mask[logic.end] if logic.end else None
                    if start_exit:
                        logicked_exits.append(start_exit)
                    if end_exit:
                        logicked_exits.append(end_exit)
                    
            unlogicked_exits = [exit for exit in room.exits if exit not in logicked_exits]

            exits_to_walk = [exit_to_search]
            while exits_to_walk:
                popped_exit = exits_to_walk.pop()
                for logic in room.logic:
                    # TODO: translate the logic on room creation
                    # TODO: translate whole room logic on room creation
                    if isinstance(logic.start, (tuple, type(None))) and isinstance(logic.end, (tuple, type(None))):
                        start_exit = room.exits_by_dir_mask[logic.start] if logic.start else None
                        end_exit = room.exits_by_dir_mask[logic.end] if logic.end else None

                        if start_exit == popped_exit:
                            opposite_exit = end_exit
                        elif end_exit == popped_exit and not logic.one_way:
                            opposite_exit = start_exit
                        else:
                            continue

                        if not opposite_exit:
                            for exit in unlogicked_exits:
                                if exit not in seen_exits:
                                    seen_exits.add(exit)
                                    if exit.locked:
                                        locked_exits.add(exit)
                                    else:
                                        other_exits.add(exit)
                                    exits_to_walk.append(exit)          
                                    
                            
                        elif opposite_exit not in seen_exits:
                            seen_exits.add(opposite_exit)
                            if opposite_exit.locked:
                                locked_exits.add(opposite_exit)
                            else:
                                other_exits.add(opposite_exit)
                            exits_to_walk.append(opposite_exit)
        else:
            for exit in room.exits:
                if exit not in seen_exits:
                    seen_exits.add(exit)
                    if exit.locked:
                        locked_exits.add(exit)
                    else:
                        other_exits.add(exit)
        for locked_exit in locked_exits:
            self.find_other_exits_for_exit(locked_exit.target.exits_by_dir_mask[(opposite_dir[locked_exit.direction], locked_exit.mask)], other_exits, seen_exits)



    def fill_other_exits_for_exit(self, exit):
        other_exits = set()
        self.find_other_exits_for_exit(exit, other_exits)
        other_exits = {other_exit for other_exit in other_exits if not other_exit.locked and other_exit != exit}
        exit.other_exits = other_exits

    
    def randomize(self, random, room_pool):
        unseen_exits = []
        # TODO: comprehension
        assert self.entrance_room in room_pool
        print("Adding everything to unseen exits")
        for room in room_pool:
            for exit in room.exits:
                unseen_exits.append(exit)

        # TODO: can we just do seen_but_unconnected?
        seen_exits = {
            Direction.Left: defaultdict(list),
            Direction.Right: defaultdict(list),
            Direction.Up: defaultdict(list),
            Direction.Down: defaultdict(list),
            Direction.Stairs: defaultdict(list),
            Direction.Drop: defaultdict(list),
            Direction.DropTarget: defaultdict(list),
            }
        
        print("Filtering out locked exits")
        
        locked_exits = [exit for exit in unseen_exits if exit.target]
        for exit in locked_exits:
            print("Seen exit: ", exit.parent.name, exit.direction, exit.mask)
            print("opposing: ", exit.target.exits)
            unseen_exits.remove(exit)
            seen_exits[exit.direction][exit.mask].append(exit)

        random.shuffle(unseen_exits)

        # TODO: assumes all exits are viable - is this true?
        
        for exit in self.entrance_room.exits:
            self.see_exit(exit, unseen_exits, seen_exits)
            
       

        def connect(a, b):
            print(f"Connecting {a.parent.name} {a.direction} {a.mask} to {b.parent.name} {b.direction} {b.mask}")
            assert not a.target, (a.parent.name, b.parent.name, a, b)
            assert not b.target, (a.parent.name, b.parent.name, a, b)
            a.target = b.parent
            b.target = a.parent

        done_with_connectors = False

        while unseen_exits:
            print(len(unseen_exits))
            for exit in unseen_exits:
                # How?!
                assert exit not in seen_exits[exit.direction][exit.mask]
                assert not exit.target, exit.parent.name

            # TODO: we need to special case lava, etc
            # TODO: just lock them together...
            
            if not done_with_connectors:
                candidate_exits = [exit for exit in unseen_exits if len(exit.other_exits) > 0]
                done_with_connectors = len(candidate_exits) == 0
                if done_with_connectors:
                    print("Done with connectors!")
            if done_with_connectors:
                for exit in unseen_exits:
                    assert not exit.other_exits
                candidate_exits = unseen_exits
            random.shuffle(candidate_exits) 
            # TODO: check if this is mathematically sound        
            for exit in candidate_exits:
                # We have a room we haven't seen before, try to link with one we have
                # print(f"Search for {exit.parent.name} {exit.direction} {exit.mask}")
                # TODO: split seen, unseen, pool
                pool = self.get_opposite_door_list(seen_exits, exit)

                # Is there a point to this?
                pool = [exit_ for exit_ in pool if not exit_.target] # and (done_with_connectors or len(exit_.other_exits) > 0)]

                if pool:
                    other_exit = random.choice(pool)
                    pool.remove(other_exit)
                    connect(exit, other_exit)
                    assert exit != other_exit
                    #old_len = len(unseen_exits)
                    assert other_exit not in unseen_exits

                    self.see_exit(exit, unseen_exits, seen_exits)
                    assert exit not in unseen_exits
                    assert other_exit not in unseen_exits
                    #assert len(unseen_exits) != old_len
                    break
                else:
                    #print(f"None found")
                    pass
            else:
                print("Ran out of seen exits that aren't connected. Remaining exits:")
                for l in seen_exits.values():
                    for k in l.values():
                        for j in k:   
                            if not j.target:
                                print('\t', j.parent.name, j.direction, j.mask)
                print("Remaining unseen exits (connectors):")
                for j in unseen_exits:
                    if j.other_exits:
                        print('\t', j.parent.name, j.direction, j.mask)
                print("Remaining unseen exits (dead ends):")
                for j in unseen_exits:
                    if not j.other_exits:
                        print('\t', j.parent.name, j.direction, j.mask)
                assert False

        
        for l in seen_exits.values():
            for mask, exits in l.items():
                l[mask] = [exit for exit in exits if not exit.target]

        for direction, l in seen_exits.items():
            for mask, exits in l.items():
                opposite_exits = seen_exits[opposite_dir[direction]][mask]
                assert len(exits) == len(opposite_exits)
                random.shuffle(exits)
                for exit, opposite_exit in zip(exits, opposite_exits):
                    connect(exit, opposite_exit)
                exits.clear()
                opposite_exits.clear()
        # TODO: somtimes this results in inaccessible items
        # probably oneways lol        

                


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
    def see_exit(self, exit_to_see, unseen_exits, seen_exits):
        if exit_to_see in seen_exits[exit_to_see.direction][exit_to_see.mask]:
            print("bail on see_exit")
            return False

        seen_exits[exit_to_see.direction][exit_to_see.mask].append(exit_to_see)
        unseen_exits.remove(exit_to_see)


        for exit in exit_to_see.other_exits:
            if exit in unseen_exits:
                print(f"seeing exit {exit_to_see.direction} {exit_to_see.mask}, adding to pool")
                seen_exits[exit.direction][exit.mask].append(exit)
                unseen_exits.remove(exit)
                assert not exit.locked

  
        # Handle any locked rooms
        # for exit in new_exits:
        #     if exit.locked:
        #         assert False
        #         self.see_exit(exit, unseen_exits, seen_exits)



    def finalize(self):
        def initialize_locations(room):
            room.location = Location(room.name, dungeon=self.dungeon_id)
            room.exit_locations = {}
            # TODO staircase, etc
            for dir, border in enumerate(room.borders):
                room.exit_locations[Direction(dir)] = []
                if isinstance(border, list):
                    for sub_border in border:
                        room.exit_locations[(dir, sub_border)] = None
                else:
                    # assert False
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
                            loc = Location(dungeon=self.dungeon_id)
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
                            room.exit_locations[key] = Location(f"{room.name} {endpoint}", dungeon=self.dungeon_id)
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
                    exit_location = room.location_for_dir_mask(exit.mask, exit.direction)
                    enter_location = exit.target.location_for_dir_mask(exit.mask, opposite_dir[exit.direction])
                    exit_location.connect(enter_location, req=None, one_way=True)

        self.walk_rooms(set_connections)

        def print_connection(room, dir, exit):
            print(f"{room.name} -> {exit.target.name}")

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
            self.walk_rooms(room_cb, connection_cb, room=exit.target, walked=walked)


class Dungeon1(Dungeon):
    def __init__(self, options, world_setup, r):
        super().__init__(1)
        
        # Rules for logic creation
        # if one room has multiple distinct parts, split them into two rooms
        # TODO: _should_ they be split? What about superjump shenanagins?
        # what happens if you jump into an area you shouldn't be in?
        # probably you just get stuck when you transition :) :) :)
        # fuck around and find out

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
        boss_key_underlook.connect(blade_block_room, Direction.Left, DoorType.Pit, locked=True)
        boss_key_underlook.connect(moldom_sparks_room, Direction.Down, DoorType.Open)
        
        spark_jump_room = Room(0x110, "Spark Jump Room", [DoorDir.LR, DoorDir.LR, TwoWideGapUD, Impassable],
                               [RoomLogic(None, FEATHER, Direction.Right)])
        spark_jump_room.connect(block_room_down, Direction.Left, DoorType.Key)

        three_kind = Room(0x10A, "D1 Three of a Kind Room", [Impassable, Impassable, Impassable, TwoWideGapUD],
                          [RoomLogic(None, r.attack_hookshot, DungeonChest(0x10A))])
        three_kind.connect(spark_jump_room, Direction.Down, DoorType.Open, DoorType.Open)

        miniboss = Room(0x111, "D1 Miniboss", [Impassable, DoorDir.LR, DoorDir.UD, Impassable],
                          [RoomLogic(Direction.Left, KillMiniboss, Direction.Up)])
        miniboss.connect(spark_jump_room, Direction.Left, DoorType.Shutter, DoorType.Open)

        boss_foyer = Room(0x10B, "D1 Boss Foyer", [Impassable, Impassable, DoorDir.UD, DoorDir.UD])
        boss_foyer.connect(miniboss, Direction.Down, DoorType.Open, DoorType.Shutter)

        boss = Room(0x106, "D1 Boss", [Impassable, Impassable, DoorDir.UD, DoorDir.UD],
                    [RoomLogic(Direction.Down, KillBoss, None),
                    RoomLogic(None, None, HeartContainer(0x106)),
                    RoomLogic(Direction.Up, KillBoss, None)])
        boss.connect(boss_foyer, Direction.Down, DoorType.Shutter, DoorType.Open)

        fail_left = Room(0x11A, "D1 Fall Left", [0b00000001, Impassable, Impassable, Impassable], two_d=True)
        boss.connect(fail_left, Direction.Drop, DoorType.Drop, DoorType.DropTarget, locked=True)
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

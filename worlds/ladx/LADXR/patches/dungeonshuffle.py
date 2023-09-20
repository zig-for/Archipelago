from ..assembler import ASM
from .. import assembler

DUNGEON_DATA_START = 0x1000

def generate_data_table(rom, dungeon):
    # TODO: set Data_014_4E41 for spawn location

    rooms = set()
    dungeon.walk_rooms(walked=rooms)

    dungeon_layout_data = bytearray(64)
    room_transition_data = bytearray(64 * 4 * 2)

    index = 0
    room_lookup = {}
    for index, room in enumerate(rooms):
        dungeon_layout_data[index] = room.room_id & 0xFF
        room_lookup[room] = index

    for index, room in enumerate(rooms):
        dungeon_layout_data[index] = room.room_id & 0xFF
        # room_lookup[room.exits[direction].room_id] = room.exits[direction]
        for exit in room.exits:
            room_transition_data[index * 8 + exit.direction * 2 + 0] = 0 # room.exits[direction].room_id & 0xFF
            room_transition_data[index * 8 + exit.direction * 2 + 1] = room_lookup[exit.target]


    dungeon_layout_size = len(dungeon_layout_data)
    dungeon_layout_start = 0x0220 + (dungeon.dungeon_id - 1) * dungeon_layout_size
    rom.banks[0x14][dungeon_layout_start : dungeon_layout_start + dungeon_layout_size] = dungeon_layout_data
    # rom.banks[0x14][0x0220] = 0x17
    # rom.banks[0x41][0x1000]
    # rom.patch(0x41, DUNGEON_DATA_START + (dungeon.dungeon_id - 1) * len(room_transition_data), old=None, new=room_transition_data)
    start = DUNGEON_DATA_START + (dungeon.dungeon_id - 1) * len(room_transition_data)
    end = start + len(room_transition_data)
    rom.banks[0x41][start : end] = room_transition_data

def patch_dungeon_logic(rom, dungeons):
    # TODO: replace with 7A4C because we don't want face shrine shenanagins
    bank2_patch_from = 0x3A67
    bank2_patch_to   = 0x3CA1
    
    rom.patch(0x02, bank2_patch_from + 1, '21AEDB181F', ASM("""jp $7CA1"""), fill_nop=True)

    labels = {}
    rom.patch(0x02, bank2_patch_to, '000000000000', ASM("""
    SwapToBank41:
        ld b, a
        ld a, $41
        ld [$2100], a
    PostSwapToBank41:
    """, bank2_patch_to + 0x4000, labels))
    
    post_swap = labels["PostSwapToBank41".upper()]

    assembler.const("PostSwapToBank41", post_swap)

    return_asm = ASM("""
        ld a, $2
        ld [$2100], a
    """)
    return_address = 0x3AA5-(len(return_asm) // 2)
    assembler.const("ReturnThunk", return_address + 0x4000)
    main_addr = 0x0
    assembler.const("MainDungeonHack", main_addr + 0x4000)
    main_asm = ASM(f"""
    ; ld hl, $DBAE
    ; ld [hl], $33
    ld a, [$DBAE] ; a = currentRoom
    sla a
    sla a
    sla a ; a *= 8                   
    add a, c
    add a, c ; a += c * 2
    add a, 1 ; skip the split byte, for now
    ld hl, $5000
    ld    e, a    ; DE = A
    ld    d, 0
    add   hl, de  ; HL = HL+DE
    ld a, [hl]
    ld [$DBAE], a
    jp ReturnThunk           
    """, base_address=main_addr + 0x4000)

    thunk_asm = ASM(f"""
    ; c = direction
    ; b = IndoorRoomIncrement[direction]
    
    ; 1. Check if we are in dungeon 1
    ldh a, [$F7]
    cp $01 ; <= dungeon1

    ; tmp
    jp c, MainDungeonHack


    ; 2. If not,
    ld a, b
    ld hl, $DBAE
    add a, [hl]
    ld [hl], a
    jp ReturnThunk
    """)

    
    while len(rom.banks) <= 0x41:
        rom.banks.append(bytearray(0x4000))
    rom.patch(0x41, post_swap - 0x4000, old=None, new=thunk_asm)

    rom.patch(0x41, return_address, old=None, new=return_asm)
    rom.patch(0x41, main_addr, old=None, new=main_asm)

    for dungeon in dungeons:
        generate_data_table(rom, dungeon)
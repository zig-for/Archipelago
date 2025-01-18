from ..assembler import ASM
import os
import pkgutil

default_pal = [0x00, 0x00,0x35, 0xad,0x52, 0x94,0x7F, 0xFF]

def updateEndScreen(rom, cat="cats/testfluffyincolor"):
    palette = default_pal
    try:
        palette = pkgutil.get_data(__name__, cat + ".pal")
    except:
        pass
    palette = [hex(i).replace("0x", "$") for i in palette]
    # Call our custom data loader in bank 3F
    rom.patch(0x00, 0x391D, ASM("""
        ld   a, $20
        ld   [$2100], a
        jp   $7de6
    """), ASM("""
        ld   a, $3F
        ld   [$2100], a
        jp   $4200
    """))
    rom.patch(0x17, 0x2FCE, "B170", "D070") # Ignore the final tile data load
    
    rom.patch(0x3F, 0x0200, None, ASM(f"""
    ; Disable LCD
    xor a
    ldh  [$40], a
    
    ld  hl, $8000
    ld  de, $5000
copyLoop:
    ld  a, [de]
    inc de
    ldi [hl], a
    bit 4, h
    jr  z, copyLoop

    ld  a, $01
    ldh [$4F], a

    ld  hl, $8000
    ld  de, $6000
copyLoop2:
    ld  a, [de]
    inc de
    ldi [hl], a
    bit 4, h
    jr  z, copyLoop2

    ld  hl, $9800
    ld  de, $0190
clearLoop1:
    xor a
    ldi [hl], a
    dec de
    ld  a, d
    or  e
    jr  nz, clearLoop1

    ld  de, $0190
clearLoop2:
    ld  a, $08
    ldi [hl], a
    dec de
    ld  a, d
    or  e
    jr  nz, clearLoop2

    xor  a
    ldh  [$4F], a


    ld  hl, $9800
    ld  de, $000C
    xor  a
loadLoop1:
    ldi  [hl], a
    ld   b, a
    ld   a, l
    and  $1F
    cp   $14
    jr   c, .noLineSkip
    add  hl, de
.noLineSkip:
    ld   a, b
    inc  a
    jr   nz, loadLoop1

loadLoop2:
    ldi  [hl], a
    ld   b, a
    ld   a, l
    and  $1F
    cp   $14
    jr   c, .noLineSkip
    add  hl, de
.noLineSkip:
    ld   a, b
    inc  a
    jr   nz, loadLoop2

    ; Load palette
    ld   hl, $DC10
    ld   a, {palette[1]}
    ldi  [hl], a
    ld   a, {palette[0]}
    ldi  [hl], a

    ld   a, {palette[3]}
    ldi  [hl], a
    ld   a, {palette[2]}
    ldi  [hl], a

    ld   a, {palette[5]}
    ldi  [hl], a
    ld   a, {palette[4]}
    ldi  [hl], a

    ld   a, {palette[7]}
    ldi  [hl], a
    ld   a, {palette[6]}
    ldi  [hl], a

    ld   a, $00
    ld   [$DDD3], a
    ld   a, $04
    ld   [$DDD4], a
    ld   a, $81
    ld   [$DDD1], a

    ; Enable LCD
    ld  a, $91
    ldh [$40], a
    ld  [$d6fd], a
    
    xor a
    ldh [$96], a
    ldh [$97], a
    ret
    """))
    
    addr = 0x1000
    data = pkgutil.get_data(__name__, cat + ".bin")    
    rom.banks[0x3F][addr : addr + len(data)] = data


import os.path
import pkgutil

def patch_vwf(rom, assembler):
    def get_asm(name):
        return pkgutil.get_data(__name__, os.path.join("vwf", name)).decode().replace("\r", "")
    assert 'saveLetterWidths' not in assembler.CONST_MAP
    assembler.resetConsts()
    assembler.const("CURR_CHAR_GFX"		,0xD608)
    assembler.const("CURR_CHAR"			,0xD638)
    assembler.const("CURR_CHAR_SIZE"		,0xD63A)
    assembler.const("IS_TILE_READY"		,0xD63B)
    assembler.const("IS_CHAR_READY"		,0xD63C)
    assembler.const("CURR_CHAR_BUFFER"	,0xD640)
    assembler.const("TILE_BUFFER"			,0xD650)
    assembler.const("wDialogBoxPosIndex"	,0xD668)
    assembler.const("wDialogBoxPosIndexHi" ,0xD669)
    assembler.const("PIXELS_TO_SUBTRACT"	,0xD66A)
    assembler.const("PIXELS_TO_ADD"		,0xD66B)
    assembler.const("wDialogCharacterIndex" ,0xC170)
    assembler.const("wDialogState" ,0xC19F)
    assembler.const("wDrawCommand.destinationHigh" , 0xD601)
    assembler.const("wDrawCommand.destinationLow" ,0xD602)
    assembler.const("wDialogNextCharPosition" ,0xC171)
    assembler.const("rSelectROMBank" , 0x2100)
    assembler.const("CodepointToTileMap" , 0x4641)

    vfw_main = 0x4000 - 332
    assembler.const("variableWidthFontThunk" , vfw_main + 0x4000)
    
    rom.patch(0x1C, vfw_main, old="00" * 332, new=assembler.ASM(get_asm("vwf.asm"), vfw_main + 0x4000))

    widthtable_size = len(assembler.ASM(get_asm("vwf_widthtable.asm"), 0x1000)) // 2

    vfw_widthtable = 0x4000 - widthtable_size
    symbols = {}
    rom.patch(0x36, vfw_widthtable, old="00" * widthtable_size, new=assembler.ASM(get_asm("vwf_widthtable.asm"), vfw_widthtable + 0x4000, symbols))
    assembler.const("saveLetterWidths", symbols["SAVELETTERWIDTHS"])
    # TODO: we may want to make sure we patch late
    font = pkgutil.get_data(__name__, "vwf/font.vwf.2bpp")
    import binascii
    font = binascii.hexlify(font)
    rom.patch(0x0F, 0x1000, old=None, new=font)
    
    # wDialogCharacterIndexHi -> wDialogBoxPosIndexHi
    rom.patch(0x00, 0x2335, '64C1', '69D6') 
    # wDialogCharacterIndex -> wDialogBoxPosIndex
    rom.patch(0x00, 0x2339, '70C1', '68D6')
    rom.patch(0x00, 0x2517, '70C1', '68D6')
    rom.patch(0x00, 0x252F, '70C1', '68D6')
    rom.patch(0x1C, 0x09F2, '70C1', '68D6')
    # " " -> "/0"
    rom.patch(0x00, 0x2607, '20', '00')


    rom.patch(0x00, 0x260B, old=assembler.ASM("""
    ld   a, $1C                                   ; $260B: $3E $1C
    ld   [rSelectROMBank], a                      ; $260D: $EA $00 $21
    ld   hl, CodepointToTileMap                   ; $2610: $21 $41 $46
    add  hl, de                                   ; $2613: $19
    ld   e, [hl]                                  ; $2614: $5E
    ld   d, $00                                   ; $2615: $16 $00
    sla  e                                        ; $2617: $CB $23
                                                        """),
    new=assembler.ASM("""
    ld   a, $36
    ld   [rSelectROMBank], a
    call saveLetterWidths
    ;ld   a, $1C                                   ; $260B: $3E $1C
    ;ld   [rSelectROMBank], a                      ; $260D: $EA $00 $21
    
                          """), fill_nop=True)
    rom.patch(0x00, 0x2646, assembler.ASM("""
        xor  a 
        pop hl
        and  a
        """),
        assembler.ASM("""jp variableWidthFontThunk"""))
    # wDialogCharacterIndex -> wDialogBoxPosIndex
    rom.patch(0x00, 0x2696, '70C1', '68D6')

    rom.patch(0x1C, 0x0641, old=assembler.ASM("""
    db  0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0

    db  0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0

    db  $7e, $3d, $41, 0  , $8a, $8b, $44, $40, $45, $46, $8c, $8d, $3a, $3f, $3b, 0

    db  $70, $71, $72, $73, $74, $75, $76, $77, $78, $79, $42, $43, $8e, 0  , $8f, $3c

    db  0  , 0  , $01, $02, $03, $04, $05, $06, $07, $08, $09, $0a, $0b, $0c, $0d, $0e

    db  $0f, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, 0  , 0  , 0  , $40, 0

    db  0  , $1a, $1b, $1c, $1d, $1e, $1f, $20, $21, $22, $23, $24, $25, $26, $27, $28

    db  $29, $2a, $2b, $2c, $2d, $2e, $2f, $30, $31, $32, $3e, 0  , 0  , 0  , 0  , 0

    db  $47, $48, $49, $4a, $4b, $4c, $4d, $4e, $4f, $50, $51, $52, $53, $59, $5a, $5b

    db  $5c, $5d, $59, $5a, $5b, $5c, $5d, $32, $6f, $6d, $6e, 0  , 0  , 0  , 0  , 0

    db  $3d, $3c, $3f, $7e, $39, $3a, $3b, $7a, $7b, 0  , 0  , 0  , 0  , 0  , 0  , 0

    db  $70, $71, $72, $73, $74, $75, $76, $77, $78, $79, $9b, $9c, $9d, $9e, $9f, $38

    db  0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0

    db  $80, $81, $82, $83, $84, $85, $86, $87, $88, $89, $8a, $8b, $8c, $8d, $8e, $8f

    db  $88, $90, $91, $92, $93, $94, $95, $89, $96, $97, $98, $99, $9a, $87, $86, 0

    db  $34, $35, $36, $37, 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , $7e, 0  , 0
                                              """), new=assembler.ASM("""
    db  $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e

    db  $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e
;  $20        !    "    #    $    %    &    '    (    )    *    +    ,    -           
    db  $7e, $3d, $41, $16, $8a, $8b, $44, $40, $45, $46, $8c, $8d, $3a, $3f, $39, $7e
;  $30   0    1    2    3    4    5    6    7    8    9    :    ;    <    =    >    ?
    db  $70, $71, $72, $73, $74, $75, $76, $77, $78, $79, $42, $43, $8e, 0  , $8f, $3c
;  $40   @    A    B    C    D    E    F    G    H    I    J    K    L    M    N    O
    db  0  , 0  , $01, $02, $03, $04, $05, $06, $07, $08, $09, $0a, $0b, $0c, $0d, $0e
;  $50   P    Q    R    S    T    U    V    W    X    Y    Z   ...   \    ]    ^    _
    db  $0f, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $6F, 0  , 0  , $40, 0
;  $60   `    a    b    c    d    e    f    g    h    i    j    k    l    m    n    o
    db  0  , $1a, $1b, $1c, $1d, $1e, $1f, $20, $21, $22, $23, $24, $25, $26, $27, $28
;  $70   p    q    r    s    t    u    v    w    x    y    z    --   |    }    ~
    db  $29, $2a, $2b, $2c, $2d, $2e, $2f, $30, $31, $32, $3e, $4e, 0  , 0  , 0  , 0
;  $80   Á    É    Í    Ó    Ú    Ü    Ñ    --   Ç    á    é    í    ó    ú    ü    ñ
    db  $47, $48, $49, $4a, $4b, $4c, $4d, $4e, $4f, $50, $51, $52, $53, $54, $55, $56
;  $90   à    è    ì    ò    ù    ä    ë    ï    ö   ...   ¡    ¿    "    '    .
    db  $57, $58, $59, $5A, $5B, $5C, $5D, $5E, $5F, $6f, $6e, $6d, $6c, $6b, $6a, 0
;  $A0   !    ?    -  BLANK  .    ,    .2   "     
    db  $3d, $3c, $3f, $7e, $39, $3a, $3b, $7a, $7b, 0  , 0  , 0  , 0  , 0  , 0  , 0
;  $B0   0    1    2    3    4    5    6    7    8    9    â    ê    î    ô    û
    db  $70, $71, $72, $73, $74, $75, $76, $77, $78, $79, $9b, $9c, $9d, $9e, $9f, $38
;  $C0   0    1    2    3    4    5    6    7    8    9  
    db  $60, $61, $62, $63, $64, $65, $66, $67, $68, $69, 0  , 0  , 0  , 0  , 0  , 0
;  $D0   A2  B2   C2   D2   E2   F2   DPAD LTTR YOSH HIBS FOOT (X)  SKUL LINK MARN TARN
    db  $80, $81, $82, $83, $84, $85, $86, $87, $88, $89, $8a, $8b, $8c, $8d, $8e, $8f
;  $E0  YOSH BOW  CAN  BANA STCK BEEH PINE BROM HOOK BRA  SCAL GLAS      LTTR DPAD
    db  $88, $90, $91, $92, $93, $94, $95, $89, $96, $97, $98, $99, $9a, $87, $86, 0
;  $F0   UP  DOWN LEFT RIGHT                                            BLANK
    db  $34, $35, $36, $37, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e
                                                        """))


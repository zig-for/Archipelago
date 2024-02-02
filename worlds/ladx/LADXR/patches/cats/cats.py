

def dumpNyanImage(cat_name="nyan", out_dir="."):
    import PIL.Image
    with open('LADXR\\patches\\' + cat_name + '.bin', 'rb') as f:
        nyan = f.read()
    img = PIL.Image.new("P", (160, 144))
    img.putpalette((
        0, 0, 0,
        155, 155, 155,
        213, 213, 213,
        255, 255, 255,
    ))
    print(len(nyan))
    tile_x_width = 20
    tile_y_height = 18
    for tx in range(tile_x_width):
        for ty in range(tile_y_height):
            for y in range(8):

                a = nyan[tx * 16 + ty * tile_x_width * 16 + y * 2]
                b = nyan[tx * 16 + ty * tile_x_width * 16 + y * 2 + 1]
                for x in range(8):
                    c = 0
                    if a & (0x80 >> x):
                        c |= 1
                    if b & (0x80 >> x):
                        c |= 2
                    img.putpixel((tx*8+x, ty*8+y), c)
    img.save(out_dir + "\\" + cat_name + ".png")

def convertCat(filename):
    import PIL.Image
    img = PIL.Image.open(filename)
    assert(len(img.getpalette()) == 12)
    img.save("test.png")

    pal = img.getpalette()
    print (f"Palette: {pal}")
    pal_bytes = []
    for pal_idx in range(0, 12, 3):
        print(pal_idx)
        r = pal[pal_idx + 0] >> 3
        g = pal[pal_idx + 1] >> 3
        b = pal[pal_idx + 2] >> 3
        rgb = r | (g << 5) | (b << 10)
        pal_bytes += [rgb >> 8, rgb & 0xFF]
    print(pal_bytes)
    assert (img.size[0] % 8) == 0
    tileheight = 8 
    print(tileheight)
    assert (img.size[1] % tileheight) == 0
    cols = img.size[0] // 8
    rows = img.size[1] // tileheight
    print(rows)
    print(cols)
    result = bytearray(rows * cols * tileheight * 2)
    index = 0
    for ty in range(rows):
        for tx in range(cols):
            for y in range(tileheight):
                a = 0
                b = 0
                for x in range(8):
                    c = img.getpixel((tx * 8 + x, ty * tileheight + y))
                    if c & 1:
                        a |= 0x80 >> x
                    if c & 2:
                        b |= 0x80 >> x
                result[index] = a
                result[index+1] = b
                index += 2
    return result, pal_bytes

cat_name = "testfluffyincolor"
with open(cat_name + ".bin", 'wb') as out:
    with open(cat_name + ".pal", 'wb') as pal_out:
        image, pal = convertCat(cat_name + ".png")
        out.write(image)
        print(len(pal))
        pal_out.write(bytearray(pal))

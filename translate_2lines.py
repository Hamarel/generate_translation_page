# importing modules

from PIL import Image, ImageDraw

img = Image.new('RGB', (1404, 1872), (255, 255, 255, 255))
draw = ImageDraw.Draw(img)

# Draw line

hanzisize = 100
half_hanzi = hanzisize / 2
wordsize = 40
margin_between = 25

cell = 3 * wordsize + hanzisize
width = ((1402 - 52) // hanzisize) * hanzisize
width_margin = (1402 - width) // 2

height = (1772 // (cell + margin_between)) * (cell + margin_between)
if ((height + cell + margin_between) < 1772):
    height = height + cell

for h in range(100, height, cell + margin_between):
    draw.line((width_margin, h, width + width_margin, h), fill=(0, 0, 0), width=2)  # (start x, start y,  end x, end y)
    draw.line((width_margin, h + wordsize, width + width_margin, h + wordsize), fill=(0, 0, 0),
              width=1)  # (start x, start
    # y,  end x, end y)
    draw.line((width_margin, h + wordsize + hanzisize, width + width_margin, h + wordsize + hanzisize), fill=(0, 0, 0),
              width=1)  # (start x, start y,  end x, end y)
    draw.line((width_margin, h + cell, width + width_margin, h + cell), fill=(0, 0, 0),
              width=2)  # (start x, start y,  end x, end y)

    # Grid
    draw.line((width_margin, h, width_margin, h + wordsize * 3 + hanzisize), fill=(0, 0, 0), width=1)  # first
    # horizontal line
    draw.line((width_margin, h + wordsize + half_hanzi, width + width_margin, h + wordsize + half_hanzi),
              fill=(192, 192, 192), width=1)  # (start x, start y,  end x, end y)
    for y in range(width_margin,width+width_margin,hanzisize):
        draw.line((y, h, y, h+wordsize+hanzisize), fill=(0,0,0), width=1)  # (start x, start y,  end x, end y)
        if (y < width+width_margin) :
            # Grid
            draw.line((y+1, h+wordsize+1, y+hanzisize-1, h + wordsize+hanzisize-1), fill=(192,192,192), width=1)  # (start x, start y,  end x, end y)
            draw.line((y+1, h + wordsize+hanzisize-1 , y + hanzisize-1, h + wordsize+1), fill=(192, 192, 192), width=1)  # (start x, start y,  end x, end y)
            draw.line((y+half_hanzi, h+wordsize+1, y+half_hanzi, h + wordsize+hanzisize-1), fill=(192,192,192), width=1)  # (start x, start y,  end x, end y)
    draw.line((width_margin + width, h, width + width_margin, h + wordsize * 3 + hanzisize), fill=(0, 0, 0),
              width=1)  # Last horizontal line
    draw.line((width_margin, h+cell-wordsize, width+width_margin, h+cell-wordsize), fill=(0,0,0), width=2)  # (start x, start y,  end x, end y)

img.show()
img.save("translation_2line.png")

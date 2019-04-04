from PIL import Image
from math import floor, sqrt

"""
Create just the top face of the cube

sprite - Base square texture
width - The width of the isometric top after transformation.
        The height of the returned image will be width / 2.
"""
def top_face(sprite, width):
    # Resize so that the diagonal is the correct length
    # given the width that I've got
    sprite_size, _ = sprite.size
    print("Sprite size: ", sprite_size)
    
    # The size the image needs to be in order to be the
    #   correct dimentions after rotation
    side_len = round(width/sqrt(2))
    print("side_len: ", side_len)
    
    sprite = sprite.resize((side_len, side_len))
    sprite.save("top_resize_1.png")
    
    large = Image.new("RGBA", (width, width), (0,0,0,0))
    large.paste(sprite)
    
    sprite = large.rotate(45)
    sprite.save("top_rotate.png")
    
    sprite = sprite.resize((width, floor(width / 2)))
    
    return sprite

"""
Create the left side of the cube

sprite - Base 16*16 texture
height - Height of the complete isometric cube.
         The height of the returned image will be 3/4 * height
"""
def side_face(sprite, height):
    pass

"""
Create a full isometric image

top, left, right - Appropriate textures
size - finished size of the square isometric image
"""
def tesselate(top, left, right, size):
    pass

if __name__ == "__main__":
    im = Image.open("testBlock.png")
    
    top = top_face(im, 24)
    
    top.save("top.png")

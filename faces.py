from enum import Enum
from math import floor, sqrt

from Augmentor.Operations import Shear
from PIL import Image

class Orientation(Enum):
    LEFT = 0
    RIGHT = 1

"""
Create just the top face of the cube

sprite - Base square texture
width - The width of the isometric top after transformation.
        The height of the returned image will be width / 2.
"""
def top_face(sprite, finish_size):
    # Resize so that the diagonal is the correct length
    # given the width that I've got
    sprite_size, _ = sprite.size
    # The size the image needs to be in order to be the
    #   correct dimentions after rotation
    side_len = round(finish_size/sqrt(2))
    
    sprite = sprite.resize((side_len, side_len))
    
    # Center the image on a transparent canvas
    large = Image.new("RGBA", (finish_size, finish_size), (0,0,0,0))
    translation = round(finish_size/2) - round(side_len/2)
    large.paste(sprite, (translation, translation))
    
    sprite = large.rotate(45)
    
    # Scale only on the y-axis
    sprite = sprite.resize((finish_size, floor(finish_size / 2)))
    
    return sprite

"""
Create the left side of the cube

sprite - Base 16*16 texture
height - Height of the complete isometric cube.
         The height of the returned image will be 3/4 * height
"""

def side_face(sprite, finish_size, orientation):
    #Resizes image to correct dimensions
    sprite_size, _ = sprite.size
    length = round(finish_size/2)
    sprite = sprite.resize((length, length))

    #Shear commands
    op = Shear(max_shear_left = 22.5)
    sprite = op.perform_operation(sprite)
    return sprite

"""
Create a full isometric image

top, left, right - Appropriate textures
size - finished size of the square isometric image
"""
def tesselate(top, left, right, size):
    base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    base.paste(top_face(top, size))
    
    base.paste(side_face(left, size), (0, size * 3/4))
    base.paste(side_face(right, size), (size / 2, size * 3/4))

if __name__ == "__main__":
    im = Image.open("testBlock.png")
    
    top = top_face(im, 24)
    
    top.save("top.png")

from enum import Enum
from math import floor, sqrt

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

    large = Image.new("RGBA",(length, round(length*1.5)), (0,0,0,0))
    large.paste(sprite, (0 , round(length*0.5)))
    large.save("intermediate.png")

    # Shear
    orient = large.transform( \
        (length, round(length*1.5)), \
        Image.AFFINE, \
        (1, 0, 0,  0.5, 1, 0))
    if Orientation.LEFT == orientation:
        orient = orient.transpose(Image.FLIP_LEFT_RIGHT)
    return orient

"""
Create a full isometric image

top, left, right - Appropriate textures
size - finished size of the square isometric image
"""
def tesselate(top, left, right, finish_size):
    base = Image.new("RGBA", (finish_size, finish_size), (0, 0, 0, 0))
    base.paste(side_face(left, finish_size, Orientation.LEFT), (0, round(finish_size * 1/4)))
    base.paste(side_face(right, finish_size, Orientation.RIGHT), (round(finish_size / 2), round(finish_size * 1/4)))
    base.alpha_composite(top_face(top, finish_size))
    return base

if __name__ == "__main__":
	#Replace path inside quotes to change blocks
    im = Image.open("testBlock.png")

    block = tesselate(im, im, im, 4096)
    block.save("block.png")

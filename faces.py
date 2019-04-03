"""
Create just the top face of the cube

sprite - Base square 16*16 texture
width - The width of the isometric top after transformation.
        The height of the returned image will be width / 2.
"""
def top_face(sprite, width):
    pass

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

top, left, right - Appropriate 16*16 textures
size - finished size of the square isometric image
"""
def tesselate(top, left, right, size):
    pass

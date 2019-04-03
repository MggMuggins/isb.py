import Image

"""
Create just the top face of the cube

sprite - Base square texture
width - The width of the isometric top after transformation.
        The height of the returned image will be width / 2.
"""
def top_face(sprite, width):
    # Resize so that the diagonal is the correct length
    # given the width that I've got
    sprite_size = sprite.size_column
    scale_factor = sqrt(width/2) / sprite_size
    side_len = sprite_size * scale_factor
    sprite.resize((side_len, side_len))
    
    sprite.rotate(45)
    
    sprite.resize((width, width / 2))
    
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
    im = Image.open("dirt.png")
    
    top = top_face(im)
    
    top.save("dirt_transformed.png")

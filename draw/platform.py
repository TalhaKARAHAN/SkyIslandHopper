from OpenGL.GL import *
from .cube import draw_textured_cube

def draw_platforms(platforms, portal_position, current_theme, platform_textures):
    glEnable(GL_TEXTURE_2D)
    for plat in platforms:
        if plat['pos'][2] < portal_position[2]:
            continue
        x, y, z = plat['pos']
        s = plat['size']
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(s, 1.5, s)
        draw_textured_cube(platform_textures[0], platform_textures[1], 1.0)
        glPopMatrix()
    glDisable(GL_TEXTURE_2D) 
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_score_with_images(score, digit_textures, x=10, y=10, scale=1.0, window_width=1920, window_height=1080):
    score_str = str(score)
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, window_width, window_height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    offset = 0
    for digit in score_str:
        if digit in digit_textures:
            tex_id, w, h = digit_textures[digit]
            w_scaled = int(w * scale)
            h_scaled = int(h * scale)
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 1); glVertex2f(x + offset, y)
            glTexCoord2f(1, 1); glVertex2f(x + offset + w_scaled, y)
            glTexCoord2f(1, 0); glVertex2f(x + offset + w_scaled, y + h_scaled)
            glTexCoord2f(0, 0); glVertex2f(x + offset, y + h_scaled)
            glEnd()
            offset += w_scaled + 2
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopAttrib()

def draw_score(score, high_score, digit_textures, window_width=1920, window_height=1080):
    draw_score_with_images(score, digit_textures, x=10, y=10, scale=0.6, window_width=window_width, window_height=window_height)
    high_score_str = str(high_score)
    total_width = 0
    for digit in high_score_str:
        if digit in digit_textures:
            w, _ = digit_textures[digit][1:]
            total_width += int(w * 0.6) + 2
    x_pos = window_width - total_width - 10
    draw_score_with_images(high_score, digit_textures, x=x_pos, y=10, scale=0.6, window_width=window_width, window_height=window_height) 
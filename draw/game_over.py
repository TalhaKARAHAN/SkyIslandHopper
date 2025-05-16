from OpenGL.GL import *
from OpenGL.GLU import *
from .score import draw_score_with_images

def draw_game_over(go_tex_id, go_tex_w, go_tex_h, textures, digit_textures, score, high_score, window_width=1920, window_height=1080):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, window_width, window_height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    highscore_tex_id, highscore_w, highscore_h = textures['highscore']
    score_tex_id, score_w, score_h = textures['score']
    common_width = max(go_tex_w, highscore_w, score_w)
    common_x = (window_width - common_width) // 2
    highscore_x = common_x
    highscore_y = (window_height - go_tex_h) // 2 - highscore_h - 30
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, highscore_tex_id)
    glColor4f(1, 1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(highscore_x, highscore_y)
    glTexCoord2f(1, 1); glVertex2f(highscore_x + highscore_w, highscore_y)
    glTexCoord2f(1, 0); glVertex2f(highscore_x + highscore_w, highscore_y + highscore_h)
    glTexCoord2f(0, 0); glVertex2f(highscore_x, highscore_y + highscore_h)
    glEnd()
    go_x = common_x
    go_y = (window_height - go_tex_h) // 2
    glBindTexture(GL_TEXTURE_2D, go_tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(go_x, go_y)
    glTexCoord2f(1, 1); glVertex2f(go_x + go_tex_w, go_y)
    glTexCoord2f(1, 0); glVertex2f(go_x + go_tex_w, go_y + go_tex_h)
    glTexCoord2f(0, 0); glVertex2f(go_x, go_y + go_tex_h)
    glEnd()
    score_x = common_x
    score_y = go_y + go_tex_h + 50
    glBindTexture(GL_TEXTURE_2D, score_tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(score_x, score_y)
    glTexCoord2f(1, 1); glVertex2f(score_x + score_w, score_y)
    glTexCoord2f(1, 0); glVertex2f(score_x + score_w, score_y + score_h)
    glTexCoord2f(0, 0); glVertex2f(score_x, score_y + score_h)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    high_score_scale = 1.0
    high_score_x = highscore_x + highscore_w + 40
    high_score_y = highscore_y + 10
    draw_score_with_images(high_score, digit_textures, x=high_score_x, y=high_score_y, scale=high_score_scale, window_width=window_width, window_height=window_height)
    score_scale = 1.0
    score_num_x = score_x + score_w + 40
    score_num_y = score_y + 10
    draw_score_with_images(score, digit_textures, x=score_num_x, y=score_num_y, scale=score_scale, window_width=window_width, window_height=window_height)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW) 
from OpenGL.GL import *
from OpenGL.GLU import *

class Coin:
    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.radius = 0.5
        self.rotation = 0
        
    def draw(self, game):
        glPushMatrix()
        glTranslatef(*self.position)
        
        # Kameraya bakacak şekilde döndür
        modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
        
        # Kamera matrisini al ve sadece rotasyonu sıfırla
        glLoadIdentity()
        glTranslatef(modelview[3][0], modelview[3][1], modelview[3][2])
        
        # Kendi ekseni etrafında döndür
        glRotatef(self.rotation, 0, 1, 0)
        
        # Texture'ı etkinleştir
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Coin texture'ını bağla
        glBindTexture(GL_TEXTURE_2D, game.textures['coin'][0])
        
        # Coin'i çiz
        glColor4f(1.0, 1.0, 1.0, 1.0)
        size = self.radius * 2
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-size/2, -size/2, 0)
        glTexCoord2f(1, 0); glVertex3f(size/2, -size/2, 0)
        glTexCoord2f(1, 1); glVertex3f(size/2, size/2, 0)
        glTexCoord2f(0, 1); glVertex3f(-size/2, size/2, 0)
        glEnd()
        
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)
        
        glPopMatrix()
        
        # Rotasyonu güncelle
        self.rotation += 2.0
        if self.rotation >= 360:
            self.rotation = 0 
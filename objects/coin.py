from OpenGL.GL import *
from OpenGL.GLU import *

class Coin:
    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.radius = 0.3

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)  # Coin'in pozisyonunu uygula
        glColor3f(1.0, 1.0, 0.0)  # Sarı renk
        quad = gluNewQuadric()
        gluSphere(quad, self.radius, 16, 16)  # Coin'i çizecek küre
        glPopMatrix() 
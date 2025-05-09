from OpenGL.GL import *
from OpenGL.GLU import *

class Portal:
    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.radius = 3.0

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)  # Portal pozisyonu
        glColor3f(0.5, 0.0, 1.0)  # Mor renk
        quad = gluNewQuadric()
        gluDisk(quad, self.radius - 0.2, self.radius, 32, 1)  # Disk şeklinde portal
        glPopMatrix()

    def update(self, delta_time):
        # Portal animasyonu
        self.rotation += 45 * delta_time
        if self.rotation >= 360:
            self.rotation = 0
        
        if self.active:
            self.animation_time += delta_time
    
    def render(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation, 0, 1, 0)
        
        # Portal çerçevesi
        glColor3f(0.0, 0.8, 1.0)  # Mavi renk
        
        # Dış halka
        glBegin(GL_LINE_LOOP)
        for i in range(32):
            angle = 2.0 * math.pi * i / 32
            x = self.size * math.cos(angle)
            z = self.size * math.sin(angle)
            glVertex3f(x, 0, z)
        glEnd()
        
        # İç halka
        glBegin(GL_LINE_LOOP)
        for i in range(32):
            angle = 2.0 * math.pi * i / 32
            x = (self.size * 0.7) * math.cos(angle)
            z = (self.size * 0.7) * math.sin(angle)
            glVertex3f(x, 0, z)
        glEnd()
        
        # Portal yüzeyi
        if self.active:
            # Aktif portal için parıltı efekti
            alpha = 0.5 + 0.5 * math.sin(self.animation_time * 5)
            glColor4f(0.0, 0.8, 1.0, alpha)
        else:
            glColor4f(0.0, 0.8, 1.0, 0.3)
        
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, 0)  # Merkez
        for i in range(33):  # 32 dilim
            angle = 2.0 * math.pi * i / 32
            x = (self.size * 0.7) * math.cos(angle)
            z = (self.size * 0.7) * math.sin(angle)
            glVertex3f(x, 0, z)
        glEnd()
        
        glPopMatrix()
    
    def check_teleport(self, player):
        if not self.active:
            return False
        
        # Oyuncu ile portal arasındaki mesafeyi kontrol et
        dx = self.position[0] - player.position[0]
        dy = self.position[1] - player.position[1]
        dz = self.position[2] - player.position[2]
        
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        return distance < self.size * 0.5  # Portal boyutunun yarısı kadar yakınlık 
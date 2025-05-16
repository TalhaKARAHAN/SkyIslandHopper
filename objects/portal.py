from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

class Portal:
    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.radius = 10  # Portal boyutunu iki katına çıkardık (5'ten 10'a)
        self.collision_radius = 6.0  # Çarpışma yarıçapını da artırdık (3.0'dan 6.0'a)
        self.color = (0.0, 1.0, 0.0)  # Yeşil
        self.animation_time = 0
        self.particles = []
        self.generate_particles()

    def generate_particles(self):
        self.particles = []
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.02, 0.05)
            self.particles.append({
                'angle': angle,
                'speed': speed,
                'distance': random.uniform(0.5, 1.5),
                'size': random.uniform(0.1, 0.3)
            })

    def update_animation(self):
        self.animation_time += 0.05
        for particle in self.particles:
            particle['angle'] += particle['speed']
            particle['distance'] += math.sin(self.animation_time) * 0.02
        
    def draw(self, animating=False, anim_time=0.0, zoom=1.0):
        glPushMatrix()
        glTranslatef(*self.position)
        # Portal animasyonu: boyut dalgalanması veya zoom
        scale = 1.0
        if animating:
            scale = zoom
        glScalef(scale, scale, scale)
        # Portal arka disk (opak)
        glColor4f(0.0, 0.0, 0.0, 1.0)
        quad = gluNewQuadric()
        gluDisk(quad, 0, self.radius, 32, 1)
        # Portal çerçevesi
        glColor3f(*self.color)
        gluDisk(quad, self.radius - 0.2, self.radius, 32, 1)  # Çerçeve kalınlığını artırdık
        # Portal içi
        glColor4f(*self.color, 0.3)
        gluDisk(quad, 0, self.radius - 0.2, 32, 1)  # İç disk boyutunu artırdık
        # Parçacıklar
        self.update_animation()
        for particle in self.particles:
            x = math.cos(particle['angle']) * particle['distance'] * 2  # Parçacık mesafesini artırdık
            y = math.sin(particle['angle']) * particle['distance'] * 2
            z = math.sin(anim_time + particle['angle']) * 0.4  # Z hareketini artırdık
            glPushMatrix()
            glTranslatef(x, y, z)
            glColor4f(*self.color, 0.6)
            gluSphere(quad, particle['size'] * 2, 8, 8)  # Parçacık boyutunu artırdık
            glPopMatrix()
        glPopMatrix()
    
    def draw_glow_effect(self):
        glPushMatrix()
        glTranslatef(*self.position)
        
        # Parlama efekti
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        for i in range(3):
            size = self.radius * (1.2 + i * 0.2)
            alpha = 0.3 - i * 0.1
            glColor4f(*self.color, alpha)
            
            quad = gluNewQuadric()
            gluDisk(quad, size - 0.1, size, 32, 1)
        
        glDisable(GL_BLEND)
        glPopMatrix()
    
    def draw_portal_depth(self):
        glPushMatrix()
        glTranslatef(*self.position)
        
        # Portal derinlik efekti
        glColor4f(*self.color, 0.2)
        for i in range(5):
            depth = -i * 0.2
            size = self.radius * (1.0 - i * 0.1)
            
            glPushMatrix()
            glTranslatef(0, 0, depth)
            quad = gluNewQuadric()
            gluDisk(quad, 0, size, 32, 1)
            glPopMatrix()
        
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
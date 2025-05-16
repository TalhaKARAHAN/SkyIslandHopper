from OpenGL.GL import *
from OpenGL.GLU import *
import math

from pygame import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP

from draw import draw_simple_cube

class Player:
    def __init__(self):
        self.position = [0, 6, 0]  # x, y, z
        self.velocity = [0, 0, 0]  # x, y, z
        self.radius = 0.5
        self.color = (1.0, 0.0, 0.0)  # Kırmızı
        self.rotation = 0
        self.is_jumping = False

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation, 0, 1, 0)

        # Gövde
        glColor3f(0.8, 0.6, 0.4)
        glPushMatrix()
        glScalef(0.4, 1.0, 0.2)
        draw_simple_cube(1)
        glPopMatrix()

        # Kafa
        glColor3f(1.0, 0.8, 0.6)
        glPushMatrix()
        glTranslatef(0, 0.7, 0)
        quad = gluNewQuadric()
        gluSphere(quad, 0.25, 16, 16)
        glPopMatrix()

        # Bacaklar
        glColor3f(0.2, 0.2, 0.8)
        for dx in [-0.15, 0.15]:
            glPushMatrix()
            glTranslatef(dx, -0.6, 0)
            glScalef(0.1, 0.5, 0.1)
            draw_simple_cube(1)
            glPopMatrix()

        # Kollar
        glColor3f(0.8, 0.6, 0.4)
        for dx in [-0.35, 0.35]:
            glPushMatrix()
            glTranslatef(dx, 0.2, 0)
            glScalef(0.1, 0.5, 0.1)
            draw_simple_cube(1)
            glPopMatrix()

        glPopMatrix()

    def update(self, gravity, jump_power, move_speed, keys):
        # Yatay hareket
        if keys[K_LEFT]:
            self.position[0] -= move_speed
            self.rotation = 90
        if keys[K_RIGHT]:
            self.position[0] += move_speed
            self.rotation = -90
        # İleri-geri hareket
        if keys[K_UP]:
            self.position[2] -= move_speed
        if keys[K_DOWN]:
            self.position[2] += move_speed
        # Zıplama
        if keys[K_SPACE] and not self.is_jumping:
            self.velocity[1] = jump_power
            self.is_jumping = True
        # Yerçekimi
        self.velocity[1] -= gravity
        self.position[1] += self.velocity[1]
        # Yere değme kontrolü
        if self.position[1] <= 4.0:  # Yer seviyesi
            self.position[1] = 4.0
            self.velocity[1] = 0
            self.is_jumping = False

    def move(self, direction):
        if self.is_dashing:
            return

        move_speed = self.speed
        if direction == "forward":
            self.velocity[2] = -move_speed
        elif direction == "backward":
            self.velocity[2] = move_speed
        elif direction == "left":
            self.velocity[0] = -move_speed
            self.rotation = 90
        elif direction == "right":
            self.velocity[0] = move_speed
            self.rotation = -90

    def jump(self):
        if self.is_grounded:
            self.velocity[1] = self.jump_force
            self.is_grounded = False
            self.double_jump_available = True
        elif self.double_jump_available:
            self.velocity[1] = self.jump_force * 0.8
            self.double_jump_available = False

    def dash(self):
        if self.dash_cooldown <= 0 and not self.is_dashing:
            self.is_dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown = 1.0  # 1 saniye bekleme süresi
            # Dash yönünü mevcut hareket yönüne göre ayarla
            if abs(self.velocity[0]) > abs(self.velocity[2]):
                self.velocity[0] = self.dash_speed * (1 if self.velocity[0] > 0 else -1)
                self.velocity[2] = 0
            else:
                self.velocity[2] = self.dash_speed * (1 if self.velocity[2] > 0 else -1)
                self.velocity[0] = 0

    def update(self, delta_time):
        # Yerçekimi uygula
        if not self.is_grounded:
            self.velocity[1] -= self.gravity * delta_time
        
        # Dash durumunu güncelle
        if self.is_dashing:
            self.dash_timer -= delta_time
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.velocity = [0, self.velocity[1], 0]
        
        # Dash cooldown'u güncelle
        if self.dash_cooldown > 0:
            self.dash_cooldown -= delta_time
        
        # Kayma durumunu güncelle
        if self.is_sliding:
            self.velocity[0] = self.slide_direction[0] * self.slide_speed
            self.velocity[2] = self.slide_direction[2] * self.slide_speed
        
        # Sürtünme uygula
        if self.is_grounded:
            self.velocity[0] *= self.friction
            self.velocity[2] *= self.friction
        
        # Pozisyonu güncelle
        self.position[0] += self.velocity[0] * delta_time
        self.position[1] += self.velocity[1] * delta_time
        self.position[2] += self.velocity[2] * delta_time
        
        # Yatay hareketi sıfırla (sürekli hareket için)
        if not self.is_sliding:
            self.velocity[0] = 0
            self.velocity[2] = 0
    
    def render(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation, 0, 1, 0)

        # Oyuncu modeli
        glColor3f(0.2, 0.6, 1.0)  # Daha koyu mavi renk
        
        # Gövde (daha yuvarlak)
        glPushMatrix()
        glScalef(0.4, 0.6, 0.3)
        self.draw_sphere(1.0)
        glPopMatrix()

        # Kafa (daha yuvarlak)
        glPushMatrix()
        glTranslatef(0, 0.5, 0)
        glScalef(0.3, 0.3, 0.3)
        self.draw_sphere(1.0)
        glPopMatrix()

        # Gözler
        glColor3f(1.0, 1.0, 1.0)  # Beyaz
        glPushMatrix()
        glTranslatef(0.1, 0.55, 0.2)
        glScalef(0.05, 0.05, 0.05)
        self.draw_sphere(1.0)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.1, 0.55, 0.2)
        glScalef(0.05, 0.05, 0.05)
        self.draw_sphere(1.0)
        glPopMatrix()

        # Göz bebekleri
        glColor3f(0.0, 0.0, 0.0)  # Siyah
        glPushMatrix()
        glTranslatef(0.1, 0.55, 0.25)
        glScalef(0.02, 0.02, 0.02)
        self.draw_sphere(1.0)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.1, 0.55, 0.25)
        glScalef(0.02, 0.02, 0.02)
        self.draw_sphere(1.0)
        glPopMatrix()

        # Kollar (daha yuvarlak)
        glColor3f(0.2, 0.6, 1.0)  # Tekrar mavi
        glPushMatrix()
        glTranslatef(0.3, 0.2, 0)
        glRotatef(45, 0, 0, 1)  # Kolları biraz açılı yap
        glScalef(0.15, 0.4, 0.15)
        self.draw_sphere(1.0)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.3, 0.2, 0)
        glRotatef(-45, 0, 0, 1)  # Kolları biraz açılı yap
        glScalef(0.15, 0.4, 0.15)
        self.draw_sphere(1.0)
        glPopMatrix()

        # Bacaklar (daha yuvarlak)
        glPushMatrix()
        glTranslatef(0.15, -0.3, 0)
        glScalef(0.15, 0.4, 0.15)
        self.draw_sphere(1.0)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.15, -0.3, 0)
        glScalef(0.15, 0.4, 0.15)
        self.draw_sphere(1.0)
        glPopMatrix()

        # Kanatlar (yeni)
        glColor3f(0.8, 0.8, 1.0)  # Açık mavi
        glPushMatrix()
        glTranslatef(0.4, 0.3, 0)
        glRotatef(30, 0, 0, 1)
        glScalef(0.2, 0.4, 0.1)
        self.draw_wing()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.4, 0.3, 0)
        glRotatef(-30, 0, 0, 1)
        glScalef(0.2, 0.4, 0.1)
        self.draw_wing()
        glPopMatrix()

        glPopMatrix()

    def draw_sphere(self, radius):
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, radius, 16, 16)

    def draw_wing(self):
        glBegin(GL_TRIANGLES)
        # Kanat üçgeni
        glVertex3f(0, 0, 0)  # Kanat kökü
        glVertex3f(1, 0.5, 0)  # Kanat ucu
        glVertex3f(0, 1, 0)  # Kanat üstü
        glEnd()

        # Kanat detayları
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0.5, 0.25, 0)
        glVertex3f(0.5, 0.25, 0)
        glVertex3f(0, 1, 0)
        glEnd()

    def draw_cube(self, size):
        vertices = [
            [-size, -size, -size], [size, -size, -size], [size, size, -size], [-size, size, -size],
            [-size, -size, size], [size, -size, size], [size, size, size], [-size, size, size]
        ]
        
        edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]
        
        glBegin(GL_QUADS)
        # Ön yüz
        glVertex3f(-size, -size, -size)
        glVertex3f(size, -size, -size)
        glVertex3f(size, size, -size)
        glVertex3f(-size, size, -size)
        
        # Arka yüz
        glVertex3f(-size, -size, size)
        glVertex3f(-size, size, size)
        glVertex3f(size, size, size)
        glVertex3f(size, -size, size)
        
        # Üst yüz
        glVertex3f(-size, size, -size)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        glVertex3f(-size, size, size)
        
        # Alt yüz
        glVertex3f(-size, -size, -size)
        glVertex3f(-size, -size, size)
        glVertex3f(size, -size, size)
        glVertex3f(size, -size, -size)
        
        # Sağ yüz
        glVertex3f(size, -size, -size)
        glVertex3f(size, -size, size)
        glVertex3f(size, size, size)
        glVertex3f(size, size, -size)
        
        # Sol yüz
        glVertex3f(-size, -size, -size)
        glVertex3f(-size, size, -size)
        glVertex3f(-size, size, size)
        glVertex3f(-size, -size, size)
        glEnd()

    def check_collision(self, other):
        # Gelişmiş küre çarpışma kontrolü
        dx = self.position[0] - other.position[0]
        dy = self.position[1] - other.position[1]
        dz = self.position[2] - other.position[2]
        
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        min_distance = self.size + other.size
        
        return distance < min_distance
    
    def handle_platform_collision(self, platform):
        # Platform çarpışma kontrolü ve tepkisi
        platform_min = [
            platform['position'][0] - platform['size'][0],
            platform['position'][1] - platform['size'][1],
            platform['position'][2] - platform['size'][2]
        ]
        platform_max = [
            platform['position'][0] + platform['size'][0],
            platform['position'][1] + platform['size'][1],
            platform['position'][2] + platform['size'][2]
        ]
        
        # Oyuncu sınırları
        player_min = [
            self.position[0] - self.size,
            self.position[1] - self.size,
            self.position[2] - self.size
        ]
        player_max = [
            self.position[0] + self.size,
            self.position[1] + self.size,
            self.position[2] + self.size
        ]
        
        # Çarpışma yönünü belirle
        overlap_x = min(player_max[0], platform_max[0]) - max(player_min[0], platform_min[0])
        overlap_y = min(player_max[1], platform_max[1]) - max(player_min[1], platform_min[1])
        overlap_z = min(player_max[2], platform_max[2]) - max(player_min[2], platform_min[2])
        
        if overlap_x > 0 and overlap_y > 0 and overlap_z > 0:
            # En küçük örtüşme yönünü bul
            if overlap_x < overlap_y and overlap_x < overlap_z:
                # X ekseninde çarpışma
                if self.position[0] < platform['position'][0]:
                    self.position[0] = platform_min[0] - self.size
                else:
                    self.position[0] = platform_max[0] + self.size
                self.velocity[0] = 0
            elif overlap_y < overlap_x and overlap_y < overlap_z:
                # Y ekseninde çarpışma
                if self.position[1] < platform['position'][1]:
                    self.position[1] = platform_min[1] - self.size
                    self.velocity[1] = 0
                else:
                    self.position[1] = platform_max[1] + self.size
                    self.is_grounded = True
                    self.velocity[1] = 0
            else:
                # Z ekseninde çarpışma
                if self.position[2] < platform['position'][2]:
                    self.position[2] = platform_min[2] - self.size
                else:
                    self.position[2] = platform_max[2] + self.size
                self.velocity[2] = 0
            
            # Platform kenarında kayma kontrolü
            if self.is_grounded and not self.is_dashing:
                edge_threshold = 0.2
                if abs(self.position[0] - platform_min[0]) < edge_threshold:
                    self.is_sliding = True
                    self.slide_direction = [-1, 0, 0]
                elif abs(self.position[0] - platform_max[0]) < edge_threshold:
                    self.is_sliding = True
                    self.slide_direction = [1, 0, 0]
                elif abs(self.position[2] - platform_min[2]) < edge_threshold:
                    self.is_sliding = True
                    self.slide_direction = [0, 0, -1]
                elif abs(self.position[2] - platform_max[2]) < edge_threshold:
                    self.is_sliding = True
                    self.slide_direction = [0, 0, 1]
                else:
                    self.is_sliding = False
            
            return True
        
        return False 
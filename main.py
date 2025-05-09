import sys
import time
import random
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from utils.texture_loader import load_texture

# === Ayarlar ===
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# === Texture'lı küp çizimi ===
def draw_textured_cube(top_tex, side_tex, size=1.0):
    half = size / 2
    
    glEnable(GL_TEXTURE_2D)
    
    # Üst yüzey
    glBindTexture(GL_TEXTURE_2D, top_tex)
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # Reset color to white for proper texture
    glTexCoord2f(0, 0); glVertex3f(-half, half, -half)
    glTexCoord2f(1, 0); glVertex3f(half, half, -half)
    glTexCoord2f(1, 1); glVertex3f(half, half, half)
    glTexCoord2f(0, 1); glVertex3f(-half, half, half)
    glEnd()
    
    # Alt yüzey ve yanlar
    glBindTexture(GL_TEXTURE_2D, side_tex)
    # Alt
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # Reset color to white for proper texture
    glTexCoord2f(0, 0); glVertex3f(-half, -half, -half)
    glTexCoord2f(1, 0); glVertex3f(half, -half, -half)
    glTexCoord2f(1, 1); glVertex3f(half, -half, half)
    glTexCoord2f(0, 1); glVertex3f(-half, -half, half)
    glEnd()
    # Ön
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-half, -half, half)
    glTexCoord2f(1, 0); glVertex3f(half, -half, half)
    glTexCoord2f(1, 1); glVertex3f(half, half, half)
    glTexCoord2f(0, 1); glVertex3f(-half, half, half)
    glEnd()
    # Arka
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-half, -half, -half)
    glTexCoord2f(1, 0); glVertex3f(half, -half, -half)
    glTexCoord2f(1, 1); glVertex3f(half, half, -half)
    glTexCoord2f(0, 1); glVertex3f(-half, half, -half)
    glEnd()
    # Sol
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-half, -half, -half)
    glTexCoord2f(1, 0); glVertex3f(-half, -half, half)
    glTexCoord2f(1, 1); glVertex3f(-half, half, half)
    glTexCoord2f(0, 1); glVertex3f(-half, half, -half)
    glEnd()
    # Sağ
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(half, -half, -half)
    glTexCoord2f(1, 0); glVertex3f(half, -half, half)
    glTexCoord2f(1, 1); glVertex3f(half, half, half)
    glTexCoord2f(0, 1); glVertex3f(half, half, -half)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

def draw_skybox(sky_tex, size=100.0):
    half = size / 2
    
    glPushMatrix()
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, sky_tex)
    glColor3f(1.0, 1.0, 1.0)  # Reset color to white for proper texture
    
    glBegin(GL_QUADS)
    # Ön
    glTexCoord2f(0, 0); glVertex3f(-half, -half, -half)
    glTexCoord2f(1, 0); glVertex3f(half, -half, -half)
    glTexCoord2f(1, 1); glVertex3f(half, half, -half)
    glTexCoord2f(0, 1); glVertex3f(-half, half, -half)
    # Arka
    glTexCoord2f(0, 0); glVertex3f(-half, -half, half)
    glTexCoord2f(1, 0); glVertex3f(half, -half, half)
    glTexCoord2f(1, 1); glVertex3f(half, half, half)
    glTexCoord2f(0, 1); glVertex3f(-half, half, half)
    # Üst
    glTexCoord2f(0, 0); glVertex3f(-half, half, -half)
    glTexCoord2f(1, 0); glVertex3f(half, half, -half)
    glTexCoord2f(1, 1); glVertex3f(half, half, half)
    glTexCoord2f(0, 1); glVertex3f(-half, half, half)
    # Alt
    glTexCoord2f(0, 0); glVertex3f(-half, -half, -half)
    glTexCoord2f(1, 0); glVertex3f(half, -half, -half)
    glTexCoord2f(1, 1); glVertex3f(half, -half, half)
    glTexCoord2f(0, 1); glVertex3f(-half, -half, half)
    # Sol
    glTexCoord2f(0, 0); glVertex3f(-half, -half, -half)
    glTexCoord2f(1, 0); glVertex3f(-half, -half, half)
    glTexCoord2f(1, 1); glVertex3f(-half, half, half)
    glTexCoord2f(0, 1); glVertex3f(-half, half, -half)
    # Sağ
    glTexCoord2f(0, 0); glVertex3f(half, -half, -half)
    glTexCoord2f(1, 0); glVertex3f(half, -half, half)
    glTexCoord2f(1, 1); glVertex3f(half, half, half)
    glTexCoord2f(0, 1); glVertex3f(half, half, -half)
    glEnd()
    
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

class Scene:
    def __init__(self, universe_id=1):
        self.universe_id = universe_id
        self.setup_textures()
        
        if universe_id == 1:
            self.setup_universe_one()
        else:
            self.setup_universe_two()

    def setup_universe_one(self):
        # Mevcut platform düzeni
        self.platforms = [
            {'pos': (0, 2, 0), 'size': 6},
            {'pos': (3, 2, -6), 'size': 4},
            {'pos': (7, 2, -12), 'size': 5},
            {'pos': (4, 2, -18), 'size': 5},
            {'pos': (0, 2, -24), 'size': 5},
            {'pos': (4, 2, -30), 'size': 4},
            {'pos': (8, 2, -36), 'size': 4},
            {'pos': (4, 2, -42), 'size': 5},
            {'pos': (0, 2, -48), 'size': 5},
            {'pos': (5, 2, -54), 'size': 4},
            {'pos': (8, 2, -60), 'size': 5},
            {'pos': (4, 2, -66), 'size': 5},
        ]
        
        self.coins = [
            Coin(1.6, 4.5, 0.2),
            Coin(3.5, 4.5, -6.5),
            Coin(7.5, 4.5, -12.8),
            Coin(4.8, 4.5, -18.2),
            Coin(0.0, 4.5, -24.3),
            Coin(4.0, 4.5, -30.6),
            Coin(8.6, 4.5, -36.0),
            Coin(4.6, 4.5, -42.4),
            Coin(1.0, 4.5, -48.1),
            Coin(5.2, 4.5, -54.2),
            Coin(8.6, 4.5, -60.1),
            Coin(4.4, 4.5, -65.6),
        ]
        
        self.portal = Portal(4, 3, -72)
        self.sky_color = (0.25, 0.65, 0.95, 1.0)  # Açık mavi gökyüzü

    def setup_universe_two(self):
        # İkinci evren - Farklı platform düzeni ve renkler
        self.platforms = [
            {'pos': (0, 2, 0), 'size': 8},
            {'pos': (-4, 3, -8), 'size': 5},
            {'pos': (4, 1, -8), 'size': 5},
            {'pos': (0, 2, -16), 'size': 6},
            {'pos': (-5, 4, -24), 'size': 4},
            {'pos': (5, 0, -24), 'size': 4},
            {'pos': (0, 2, -32), 'size': 7},
            {'pos': (-6, 1, -40), 'size': 5},
            {'pos': (6, 3, -40), 'size': 5},
            {'pos': (0, 2, -48), 'size': 6},
            {'pos': (-4, 4, -56), 'size': 4},
            {'pos': (4, 0, -56), 'size': 4},
        ]
        
        self.coins = [
            Coin(0.0, 5.0, 0.0),
            Coin(-4.0, 6.0, -8.0),
            Coin(4.0, 4.0, -8.0),
            Coin(0.0, 5.0, -16.0),
            Coin(-5.0, 7.0, -24.0),
            Coin(5.0, 3.0, -24.0),
            Coin(0.0, 5.0, -32.0),
            Coin(-6.0, 4.0, -40.0),
            Coin(6.0, 6.0, -40.0),
            Coin(0.0, 5.0, -48.0),
            Coin(-4.0, 7.0, -56.0),
            Coin(4.0, 3.0, -56.0),
        ]
        
        self.portal = Portal(0, 3, -64)
        self.sky_color = (0.15, 0.15, 0.35, 1.0)  # Koyu mavi/mor gökyüzü

    def setup_textures(self):
        self.textures = {
            'top': load_texture('assets/textures/block_top.png'),
            'side': load_texture('assets/textures/block_side.png'),
            'full': load_texture('assets/textures/block_full.png'),
            'sand': load_texture('assets/textures/gravelly_sand_diff_4k.jpg'),
            'ice': load_texture('assets/textures/ice.jpg'),
            'sky': load_texture('assets/textures/sky.png'),
            'coin': load_texture('assets/textures/Coin.png'),
        }
        # Sınıf değişkeni olarak da kaydet
        Scene.textures = self.textures

    def render(self):
        # Gökyüzü rengini ayarla
        glClearColor(*self.sky_color)
        
        # Gökyüzü
        draw_skybox(self.textures['sky'])
        
        # Platformlar
        glEnable(GL_TEXTURE_2D)
        for plat in self.platforms:
            x, y, z = plat['pos']
            s = plat['size']
            glPushMatrix()
            glTranslatef(x, y, z)
            glScalef(s, 1.5, s)
            
            # İkinci evrende farklı texture'lar kullan
            if self.universe_id == 2:
                draw_textured_cube(self.textures['ice'], self.textures['ice'], 1.0)
            else:
                draw_textured_cube(self.textures['top'], self.textures['side'], 1.0)
            
            glPopMatrix()
        glDisable(GL_TEXTURE_2D)

        # Coinler
        for coin in self.coins:
            coin.draw()

        # Portal
        self.portal.draw()

class Player:
    def __init__(self):
        self.position = [0.0, 4.0, 0.0]
        self.radius = 0.5
    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glColor3f(0.9, 0.1, 0.1)  # Kırmızı
        quad = gluNewQuadric()
        gluCylinder(quad, self.radius, self.radius, 1.0, 24, 1)
        glTranslatef(0, 0, 1.0)
        gluDisk(quad, 0, self.radius, 24, 1)  # Üst kapak
        glPopMatrix()

class Coin:
    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.radius = 0.5  # Coin boyutunu 0.3'ten 0.5'e çıkardık
        self.rotation = 0
        
    def draw(self):
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
        glBindTexture(GL_TEXTURE_2D, Scene.textures['coin'])
        
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

class Portal:
    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.radius = 1.5        # Radius'u 0.8'den 1.5'e çıkardık
        self.rotation = 0
        self.inner_radius = 1.2  # İç radius'u da büyüttük
        self.height = 3.0        # Yüksekliği artırdık
        self.animation_speed = 2.0
        self.glow_intensity = 0.0
        self.glow_direction = 1
        self.collision_radius = 2.5  # Çarpışma kontrolü için daha geniş bir alan
        
    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        
        # Portal'ın etrafında parıldayan halka efekti
        self.draw_glow_effect()
        
        # Ana portal halkası
        glRotatef(-90, 1, 0, 0)  # Dikey konuma getir
        glRotatef(self.rotation, 0, 0, 1)  # Kendi etrafında döndür
        
        # Dış halka (mor)
        glColor4f(0.6, 0.2, 1.0, 0.9)
        quad = gluNewQuadric()
        gluDisk(quad, self.inner_radius, self.radius, 32, 1)
        
        # İç kısım (açık mor)
        glColor4f(0.8, 0.5, 1.0, 0.7)
        gluDisk(quad, 0, self.inner_radius, 32, 1)
        
        # Portal tünel efekti
        self.draw_portal_depth()
        
        glPopMatrix()
        
        # Animasyonu güncelle
        self.update_animation()
    
    def draw_glow_effect(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glow_radius = self.radius + 0.4  # Işıma efektini de büyüttük
        glRotatef(-90, 1, 0, 0)
        
        # Dış ışıma halkası
        glColor4f(0.6, 0.2, 1.0, 0.2 + self.glow_intensity * 0.3)
        quad = gluNewQuadric()
        gluDisk(quad, self.radius, glow_radius, 32, 1)
        
        glDisable(GL_BLEND)
    
    def draw_portal_depth(self):
        glEnable(GL_BLEND)
        depth_layers = 6  # Derinlik katmanı sayısını artırdık
        layer_spacing = 0.15
        alpha_step = 0.12
        
        for i in range(depth_layers):
            glPushMatrix()
            glTranslatef(0, 0, -i * layer_spacing)
            glColor4f(0.8, 0.5, 1.0, 0.7 - i * alpha_step)
            quad = gluNewQuadric()
            scale = 1.0 - i * 0.12  # Derinlik azalma oranını düşürdük
            gluDisk(quad, 0, self.inner_radius * scale, 32, 1)
            glPopMatrix()
        
        glDisable(GL_BLEND)
    
    def update_animation(self):
        self.rotation += self.animation_speed
        if self.rotation >= 360:
            self.rotation = 0
            
        self.glow_intensity += 0.02 * self.glow_direction
        if self.glow_intensity >= 1.0:
            self.glow_direction = -1
        elif self.glow_intensity <= 0.0:
            self.glow_direction = 1

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Sky Island Hopper")
        self.clock = pygame.time.Clock()

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Texture filtreleme ayarları
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        self.reset_game(universe_id=1)

    def reset_game(self, universe_id):
        self.score = 0
        self.player = Player()
        self.player_vel = [0, 0, 0]
        self.gravity = 0.02
        self.jump_power = 0.5
        self.on_ground = False
        self.move_speed = 0.15
        self.game_over = False
        self.current_universe = universe_id

        # Scene'i yükle
        self.scene = Scene(universe_id)
        self.platforms = self.scene.platforms
        self.coins = self.scene.coins
        self.portal = self.scene.portal

    def handle_portal_collision(self):
        if self.distance(self.player.position, self.portal.position) < self.portal.collision_radius:
            if self.current_universe == 1:
                # İlk evrenden ikinci evrene geçiş
                self.transition_to_universe(2)
            else:
                # İkinci evrenden oyunu bitir
                self.game_over = True

    def transition_to_universe(self, universe_id):
        # Skoru koru, ama diğer her şeyi sıfırla
        current_score = self.score
        self.reset_game(universe_id)
        self.score = current_score  # Skoru geri yükle

    def update_physics(self, keys):
        if self.game_over: return
        dx = dz = 0
        if keys[K_a]: dx -= self.move_speed
        if keys[K_d]: dx += self.move_speed
        if keys[K_w]: dz -= self.move_speed
        if keys[K_s]: dz += self.move_speed
        self.player.position[0] += dx
        self.player.position[2] += dz

        if not self.on_ground: self.player_vel[1] -= self.gravity
        self.player.position[1] += self.player_vel[1]
        self.on_ground = False

        # Platform çarpışmaları
        for plat in self.platforms:
            x, y, z = plat['pos']
            s = plat['size']
            px, py, pz = self.player.position
            platform_height = 1.5
            
            if (abs(px - x) < s/2 and 
                abs(pz - z) < s/2):
                if (py - self.player.radius <= y + platform_height and 
                    py >= y + platform_height/2 and 
                    self.player_vel[1] <= 0):
                    self.player.position[1] = y + platform_height + self.player.radius
                    self.player_vel[1] = 0
                    self.on_ground = True
                elif (py + self.player.radius >= y and 
                      py - self.player.radius <= y + platform_height):
                    self.player.position[1] = y - self.player.radius
                    self.player_vel[1] = 0

        # Coin toplama
        for coin in self.coins[:]:
            if self.distance(self.player.position, coin.position) < self.player.radius + coin.radius:
                self.coins.remove(coin)
                self.score += 10

        # Portal kontrolü
        self.handle_portal_collision()
            
        # Düşme kontrolü
        if self.player.position[1] < -5:
            self.game_over = True

    def draw_player(self): self.player.draw()
    def draw_coins(self): [coin.draw() for coin in self.coins]
    def draw_portal(self): self.portal.draw()

    def draw_platforms(self):
        glEnable(GL_TEXTURE_2D)
        for plat in self.platforms:
            x, y, z = plat['pos']
            s = plat['size']
            glPushMatrix()
            glTranslatef(x, y, z)
            glScalef(s, 1.5, s)
            draw_textured_cube(self.scene.textures['top'], self.scene.textures['side'], 1.0)
            glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        px, py, pz = self.player.position
        gluLookAt(px, py + 8, pz + 12, px + 1, py - 1, pz - 2, 0, 1, 0)

        # Scene'i çiz
        self.scene.render()
        self.draw_player()

        # === SKOR GÖSTERİMİ Pygame ile ===
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont('Arial', 28)
        score_text = font.render(f"Skor: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def draw_game_over(self):
        screen = pygame.display.get_surface()
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        font = pygame.font.SysFont('Arial', 48)
        text = font.render(f"GAME OVER - Skor: {self.score}", True, (255, 255, 255))
        screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2 - 50))
        restart_font = pygame.font.SysFont('Arial', 36)
        restart_text = restart_font.render("Devam etmek için bir tuşa bas", True, (255, 255, 255))
        screen.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, WINDOW_HEIGHT//2 + 30))
        pygame.display.flip()

    def distance(self, a, b): return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))

    def run(self):
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()
                if event.type == KEYDOWN:
                    if self.game_over:
                        self.__init__(); continue
                    if event.key == K_SPACE and self.on_ground:
                        self.player_vel[1] = self.jump_power
                        self.on_ground = False
            self.update_physics(keys)
            self.render()
            if self.game_over:
                self.draw_game_over()
                time.sleep(1.5)
            self.clock.tick(FPS)

if __name__ == "__main__":
    glutInit(sys.argv)
    Game().run()

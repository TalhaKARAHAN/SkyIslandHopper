from OpenGL.GL import *
from OpenGL.GLU import *
from utils.texture_loader import load_texture
from objects.portal import Portal
from objects.coin import Coin
from objects.player import Player
import math

class Scene2:
    def __init__(self):
        self.platforms = [
            # Başlangıç platformu (buzlu)
            {'pos': (0, 0, 0), 'size': 7, 'height': 0},
            
            # Orta platformlar (farklı boyutlar ve yükseklikler)
            {'pos': (5, 3, -4), 'size': 4, 'height': 3},
            {'pos': (-4, 4, -6), 'size': 5, 'height': 4},
            {'pos': (3, 5, -8), 'size': 3, 'height': 5},
            {'pos': (-2, 6, -10), 'size': 6, 'height': 6},
            
            # Zorlu platformlar
            {'pos': (4, 7, -12), 'size': 4, 'height': 7},
            {'pos': (-3, 8, -14), 'size': 3, 'height': 8},
            {'pos': (2, 9, -16), 'size': 5, 'height': 9},
        ]
        
        # Coin'leri platformların üzerine ve etrafına yerleştir
        self.coins = [
            # Başlangıç platformu coinleri
            Coin(2, 1, 2),
            Coin(-2, 1, -2),
            Coin(0, 1, 3),
            
            # Orta platform coinleri
            Coin(5, 4, -4),
            Coin(6, 4, -3),
            Coin(4, 4, -5),
            
            Coin(-4, 5, -6),
            Coin(-5, 5, -7),
            Coin(-3, 5, -5),
            
            Coin(3, 6, -8),
            Coin(4, 6, -9),
            Coin(2, 6, -7),
            
            # Zorlu platform coinleri
            Coin(4, 8, -12),
            Coin(5, 8, -13),
            Coin(3, 8, -11),
            
            Coin(-3, 9, -14),
            Coin(-4, 9, -15),
            Coin(-2, 9, -13),
            
            Coin(2, 10, -16),
            Coin(3, 10, -17),
            Coin(1, 10, -15),
        ]

        # Portal'ı en yüksek platformun üzerine yerleştir
        self.portal = Portal(2, 10, -16)
        self.textures = {}
        self.setup_scene()
    
    def setup_scene(self):
        # Texture'ları yükle
        self.textures['ice'] = load_texture('assets/textures/ice.jpg')
        self.textures['sky'] = load_texture('assets/textures/sky.png')
        
        # Adaları oluştur
        self.create_islands()
        
        # Coin'leri yerleştir
        self.place_coins()
        
        # Portal'ı yerleştir
        self.place_portal()
    
    def create_islands(self):
        # Ana ada
        self.platforms.append({'pos': (0, 0, 0), 'size': 5})
        
        # Yan adalar
        self.platforms.append({'pos': (8, 0, 8), 'size': 3})
        self.platforms.append({'pos': (-8, 0, 8), 'size': 3})
        self.platforms.append({'pos': (8, 0, -8), 'size': 3})
        self.platforms.append({'pos': (-8, 0, -8), 'size': 3})
    
    def place_coins(self):
        # Her adanın üzerine coin yerleştir
        for platform in self.platforms:
            x, y, z = platform['pos']
            # Bazı adalara birden fazla coin koy
            if platform['size'] > 3:  # Ana ada
                self.coins.append(Coin(x - 1, y + 1, z))
                self.coins.append(Coin(x + 1, y + 1, z))
            else:
                self.coins.append(Coin(x, y + 1, z))
    
    def place_portal(self):
        # Portal'ı en uzak adaya yerleştir
        self.portal = Portal(2, 0, -6)
    
    def render_island(self, platform):
        glPushMatrix()
        glTranslatef(*platform['pos'])
        
        # Ada texture'ını uygula
        bind_texture(self.textures['ice'])
        
        # Adanın üst yüzeyi
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-platform['size'], 0, -platform['size'])
        glTexCoord2f(1, 0); glVertex3f(platform['size'], 0, -platform['size'])
        glTexCoord2f(1, 1); glVertex3f(platform['size'], 0, platform['size'])
        glTexCoord2f(0, 1); glVertex3f(-platform['size'], 0, platform['size'])
        glEnd()
        
        # Adanın kenarları
        glBegin(GL_QUAD_STRIP)
        glVertex3f(-platform['size'], -platform['size'], -platform['size'])
        glVertex3f(-platform['size'], 0, -platform['size'])
        glVertex3f(platform['size'], -platform['size'], -platform['size'])
        glVertex3f(platform['size'], 0, -platform['size'])
        glVertex3f(platform['size'], -platform['size'], platform['size'])
        glVertex3f(platform['size'], 0, platform['size'])
        glVertex3f(-platform['size'], -platform['size'], platform['size'])
        glVertex3f(-platform['size'], 0, platform['size'])
        glVertex3f(-platform['size'], -platform['size'], -platform['size'])
        glVertex3f(-platform['size'], 0, -platform['size'])
        glEnd()
        
        glPopMatrix()
    
    def render_skybox(self):
        # Basit bir gökyüzü
        glPushMatrix()
        bind_texture(self.textures['sky'])
        
        # Gökyüzü küresi
        quad = gluNewQuadric()
        gluQuadricTexture(quad, True)
        gluSphere(quad, 50, 32, 32)
        
        glPopMatrix()
    
    def render(self):
        # Gökyüzünü çiz
        self.render_skybox()
        
        # Adaları çiz
        for platform in self.platforms:
            glPushMatrix()
            glTranslatef(platform['pos'][0], platform['pos'][1], platform['pos'][2])
            
            # Texture'ı uygula
            if platform['pos'] in self.textures:
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.textures[platform['pos']])
            
            # Ada modelini çiz
            glColor3f(1.0, 1.0, 1.0)
            glBegin(GL_QUADS)
            # Üst yüz
            glTexCoord2f(0, 0); glVertex3f(-platform['size'], platform['size'], -platform['size'])
            glTexCoord2f(1, 0); glVertex3f(platform['size'], platform['size'], -platform['size'])
            glTexCoord2f(1, 1); glVertex3f(platform['size'], platform['size'], platform['size'])
            glTexCoord2f(0, 1); glVertex3f(-platform['size'], platform['size'], platform['size'])
            glEnd()
            
            glDisable(GL_TEXTURE_2D)
            glPopMatrix()
        
        # Coin'leri çiz
        for coin in self.coins:
            coin.render()
        
        # Portal'ı çiz
        if self.portal:
            self.portal.render()
    
    def update(self, delta_time):
        # Coin'leri güncelle
        for coin in self.coins:
            coin.update(delta_time)
        
        # Portal'ı güncelle
        if self.portal:
            self.portal.update(delta_time)
    
    def check_collisions(self, player):
        # Ada çarpışma kontrolü
        for platform in self.platforms:
            if self.check_island_collision(player, platform):
                return "landed"
        
        # Portal çarpışma kontrolü
        if self.portal and self.portal.check_teleport(player):
            return "teleport"
        
        return None
    
    def check_island_collision(self, player, platform):
        # Basit AABB çarpışma kontrolü
        player_min = [
            player.position[0] - player.size,
            player.position[1] - player.size,
            player.position[2] - player.size
        ]
        player_max = [
            player.position[0] + player.size,
            player.position[1] + player.size,
            player.position[2] + player.size
        ]
        
        platform_min = [
            platform['pos'][0] - platform['size'],
            platform['pos'][1] - platform['size'],
            platform['pos'][2] - platform['size']
        ]
        platform_max = [
            platform['pos'][0] + platform['size'],
            platform['pos'][1] + platform['size'],
            platform['pos'][2] + platform['size']
        ]
        
        return (player_min[0] <= platform_max[0] and player_max[0] >= platform_min[0] and
                player_min[1] <= platform_max[1] and player_max[1] >= platform_min[1] and
                player_min[2] <= platform_max[2] and player_max[2] >= platform_min[2]) 

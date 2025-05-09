from OpenGL.GL import *
from OpenGL.GLU import *
from utils.texture_loader import load_texture
from objects.coin import Coin
from objects.portal import Portal
from objects.player import Player
import math

# Sabit değerler
WORLD_SIZE = 50.0
ISLAND_SPACING = 8.0
MIN_ISLAND_SIZE = 3.0
MAX_ISLAND_SIZE = 5.0
PLAYER_START_HEIGHT = 5.0

class Scene1:
    def __init__(self):
        self.platforms = [
            # Başlangıç platformu (büyük ve düz)
            {'pos': (0, 0, 0), 'size': 8, 'height': 0},
            
            # Orta platformlar (farklı boyutlar ve yükseklikler)
            {'pos': (4, 2, -4), 'size': 5, 'height': 2},
            {'pos': (-3, 3, -6), 'size': 4, 'height': 3},
            {'pos': (6, 4, -8), 'size': 3, 'height': 4},
            {'pos': (-2, 5, -10), 'size': 6, 'height': 5},
            
            # Zorlu platformlar
            {'pos': (3, 6, -12), 'size': 4, 'height': 6},
            {'pos': (-4, 7, -14), 'size': 3, 'height': 7},
            {'pos': (5, 8, -16), 'size': 5, 'height': 8},
        ]

        # Coin'leri platformların üzerine ve etrafına yerleştir
        self.coins = [
            # Başlangıç platformu coinleri
            Coin(2, 1, 2),
            Coin(-2, 1, -2),
            Coin(0, 1, 3),
            
            # Orta platform coinleri
            Coin(4, 3, -4),
            Coin(6, 3, -3),
            Coin(2, 3, -5),
            
            Coin(-3, 4, -6),
            Coin(-4, 4, -7),
            Coin(-2, 4, -5),
            
            Coin(6, 5, -8),
            Coin(7, 5, -9),
            Coin(5, 5, -7),
            
            # Zorlu platform coinleri
            Coin(3, 7, -12),
            Coin(4, 7, -13),
            Coin(2, 7, -11),
            
            Coin(-4, 8, -14),
            Coin(-5, 8, -15),
            Coin(-3, 8, -13),
            
            Coin(5, 9, -16),
            Coin(6, 9, -17),
            Coin(4, 9, -15),
        ]
        
        # Portal'ı en yüksek platformun üzerine yerleştir
        self.portal = Portal(5, 9, -16)
        
        self.textures = {}
        self.setup_scene()
    
    def setup_scene(self):
        # Texture'ları yükle
        self.textures['grass'] = load_texture('assets/textures/block_top.png')
        self.textures['sky'] = load_texture('assets/textures/sky.png')
        self.textures['sand'] = load_texture('assets/textures/gravelly_sand_diff_4k.jpg')
        
        # Adaları oluştur
        self.create_islands()
        
        # Coin'leri yerleştir
        self.place_coins()
        
        # Portal'ı yerleştir
        self.place_portal()
    
    def create_islands(self):
        # Ana ada (merkez)
        self.islands = []
        self.islands.append({
            'position': [0, -2, 0],
            'size': [MAX_ISLAND_SIZE * 2, 1, MAX_ISLAND_SIZE * 2],
            'texture': 'grass'
        })
        
        # Köşe adaları
        corner_positions = [
            [ISLAND_SPACING, -2, ISLAND_SPACING],
            [-ISLAND_SPACING, -2, ISLAND_SPACING],
            [ISLAND_SPACING, -2, -ISLAND_SPACING],
            [-ISLAND_SPACING, -2, -ISLAND_SPACING]
        ]
        
        for pos in corner_positions:
            self.islands.append({
                'position': [pos[0], -2, pos[2]],
                'size': [MIN_ISLAND_SIZE * 2, 1, MIN_ISLAND_SIZE * 2],
                'texture': 'sand'
            })
        
        # Ara adalar (köşeler arası)
        mid_positions = [
            [ISLAND_SPACING/2, -2, ISLAND_SPACING/2],
            [-ISLAND_SPACING/2, -2, ISLAND_SPACING/2],
            [ISLAND_SPACING/2, -2, -ISLAND_SPACING/2],
            [-ISLAND_SPACING/2, -2, -ISLAND_SPACING/2]
        ]
        
        for pos in mid_positions:
            self.islands.append({
                'position': [pos[0], -2, pos[2]],
                'size': [MIN_ISLAND_SIZE * 2, 1, MIN_ISLAND_SIZE * 2],
                'texture': 'sand'
            })
    
    def place_coins(self):
        # Her adanın üzerine coin yerleştir
        for island in self.islands:
            x, y, z = island['position']
            # Adanın merkezine coin koy
            self.coins.append(Coin(x, y + 1, z))
            # Adanın kenarlarına da coin koy
            size = island['size'][0]
            self.coins.append(Coin(x + size/2, y + 1, z))
            self.coins.append(Coin(x - size/2, y + 1, z))
            self.coins.append(Coin(x, y + 1, z + size/2))
            self.coins.append(Coin(x, y + 1, z - size/2))
    
    def place_portal(self):
        # Portal'ı en uzak adaya yerleştir
        self.portal = Portal(ISLAND_SPACING, 1, ISLAND_SPACING)
    
    def render(self):
        # Gökyüzünü çiz
        self.render_skybox()
        
        # Ortada büyük bir zemin çiz (test için)
        glColor3f(0.1, 0.7, 0.1)  # Daha koyu yeşil
        glBegin(GL_QUADS)
        glVertex3f(-30, -2, -30)
        glVertex3f(30, -2, -30)
        glVertex3f(30, -2, 30)
        glVertex3f(-30, -2, 30)
        glEnd()
        
        # Adaları çiz
        for i, island in enumerate(self.islands):
            glPushMatrix()
            glTranslatef(island['position'][0], island['position'][1], island['position'][2])
            # Texture'ı devre dışı bırak, parlak renk kullan
            if i == 0:
                glColor3f(1.0, 0.0, 0.0)  # Ana ada: kırmızı
            else:
                glColor3f(0.0, 0.0, 1.0)  # Yan adalar: mavi
            self.draw_island(island['size'])
            glPopMatrix()
        
        # Coin'leri çiz
        for coin in self.coins:
            coin.render()
        
        # Portal'ı çiz
        if self.portal:
            self.portal.render()
    
    def draw_island(self, size):
        # Sadece büyük bir kutu çiz (test için)
        glBegin(GL_QUADS)
        # Üst yüz
        glVertex3f(-size[0], size[1], -size[2])
        glVertex3f(size[0], size[1], -size[2])
        glVertex3f(size[0], size[1], size[2])
        glVertex3f(-size[0], size[1], size[2])
        # Alt yüz
        glVertex3f(-size[0], -size[1], -size[2])
        glVertex3f(size[0], -size[1], -size[2])
        glVertex3f(size[0], -size[1], size[2])
        glVertex3f(-size[0], -size[1], size[2])
        glEnd()
    
    def render_skybox(self):
        # Basit bir gökyüzü
        glPushMatrix()
        load_texture(self.textures['sky'])
        
        # Gökyüzü küresi
        quad = gluNewQuadric()
        gluQuadricTexture(quad, True)
        gluSphere(quad, WORLD_SIZE/2, 32, 32)
        
        glPopMatrix()
    
    def update(self, delta_time):
        # Her sahne için oyun mekaniği burada işlenebilir.
        pass

    def check_collisions(self, player):
        # Çarpışma kontrolü
        pass
    
    def check_island_collision(self, player, island):
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
        
        island_min = [
            island['position'][0] - island['size'][0],
            island['position'][1] - island['size'][1],
            island['position'][2] - island['size'][2]
        ]
        island_max = [
            island['position'][0] + island['size'][0],
            island['position'][1] + island['size'][1],
            island['position'][2] + island['size'][2]
        ]
        
        return (player_min[0] <= island_max[0] and player_max[0] >= island_min[0] and
                player_min[1] <= island_max[1] and player_max[1] >= island_min[1] and
                player_min[2] <= island_max[2] and player_max[2] >= island_min[2]) 

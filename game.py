import random
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from utils.texture_loader import load_texture, create_default_texture
from objects.player import Player
from objects.coin import Coin
from objects.portal import Portal
from utils.score import load_high_score, save_high_score
from draw import draw_simple_cube, draw_textured_cube, draw_skybox, draw_platforms, draw_game_over, draw_score_with_images, draw_score, draw_fade

glutInit()

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS = 60
PLATFORM_GENERATION_DISTANCE = 100
PLATFORM_REMOVE_DISTANCE = -20

class Theme:
    def __init__(self, name, sky_color, platform_textures, coin_texture, portal_color):
        self.name = name
        self.sky_color = sky_color
        self.platform_textures = platform_textures
        self.coin_texture = coin_texture
        self.portal_color = portal_color

# --- Game sınıfı ---
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Portal Runner")
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 10, 0, 1))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glEnable(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        self.textures = self.setup_textures()
        global game
        game = self
        self.difficulty = 0
        self.fade_alpha = 0.0
        self.reset_game()
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.go_tex_id, self.go_tex_w, self.go_tex_h = self.load_game_over_texture()
        self.load_digit_textures()
        self.transition_active = False
        self.transition_time = 0.0
        self.transition_max = 1.0

    def setup_textures(self):
        textures = {}
        texture_files = {
            'block_top': 'assets/textures/block_top.png',
            'block_side': 'assets/textures/block_side.png',
            'block_full': 'assets/textures/block_full.png',
            'sand': 'assets/textures/gravelly_sand_diff_4k.jpg',
            'ice': 'assets/textures/ice.jpg',
            'sky': 'assets/textures/sky.png',
            'coin': 'assets/textures/Coin.png',
            'highscore': 'assets/textures/highscore.png',
            'score': 'assets/textures/score.png'
        }
        for name, path in texture_files.items():
            try:
                texture_surface = pygame.image.load(path)
                texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
                width = texture_surface.get_width()
                height = texture_surface.get_height()
                texture_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, texture_id)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                textures[name] = (texture_id, width, height)
            except Exception as e:
                print(f"Texture yüklenirken hata: {path} - {str(e)}")
                default_id = create_default_texture()
                textures[name] = (default_id, 64, 64)
        return textures

    def setup_themes(self):
        return [
            Theme("Forest", (0.25, 0.65, 0.95, 1.0), 
                  [self.textures['block_top'], self.textures['block_side']],
                  self.textures['coin'],
                  (0.0, 1.0, 0.0)),
            Theme("Desert", (0.95, 0.87, 0.73, 1.0),
                  [self.textures['sand'], self.textures['sand']],
                  self.textures['coin'],
                  (1.0, 0.5, 0.0)),
            Theme("Ice", (0.8, 0.9, 1.0, 1.0),
                  [self.textures['ice'], self.textures['ice']],
                  self.textures['coin'],
                  (0.0, 0.8, 1.0))
        ]

    def reset_game(self):
        self.score = 0
        self.high_score = load_high_score()
        self.player = Player()
        self.jump_power = 0.5
        self.gravity = 0.02
        self.move_speed = 0.25
        self.game_over = False
        self.current_theme = 0
        self.themes = self.setup_themes()
        self.platforms = []
        self.coins = []
        self.portal = None
        self.generate_initial_platforms()
        first_platform = self.platforms[0]['pos']
        self.player.position = [first_platform[0], first_platform[1] + 3, first_platform[2]]

    def generate_platform(self, prev_direction='forward', prev_x=0, prev_z=0):
        size = max(7.0 - self.difficulty * 0.5, 4.5)
        y_pos = 0
        turn_chance = 0.2
        if random.random() < turn_chance:
            direction = random.choice(['left', 'right'])
        else:
            direction = 'forward'
        if prev_direction == 'forward':
            if direction == 'forward':
                x_pos = prev_x
                z_pos = prev_z - size
            elif direction == 'left':
                x_pos = prev_x - size
                z_pos = prev_z
            elif direction == 'right':
                x_pos = prev_x + size
                z_pos = prev_z
        elif prev_direction == 'left':
            x_pos = prev_x
            z_pos = prev_z - size
            direction = 'forward'
        elif prev_direction == 'right':
            x_pos = prev_x
            z_pos = prev_z - size
            direction = 'forward'
        platform = {
            'pos': (x_pos, y_pos, z_pos),
            'size': size,
            'direction': direction
        }
        coin = Coin(x_pos, y_pos + 2.5, z_pos)
        return platform, coin, direction, x_pos, z_pos

    def update_platforms(self, player_z):
        last_platform = self.platforms[-1]
        last_x, _, last_z = last_platform['pos']
        last_direction = last_platform.get('direction', 'forward')
        while last_z > player_z - PLATFORM_GENERATION_DISTANCE:
            platform, coin, last_direction, last_x, last_z = self.generate_platform(last_direction, last_x, last_z)
            self.platforms.append(platform)
            self.coins.append(coin)
        while self.platforms[0]['pos'][2] < player_z + PLATFORM_REMOVE_DISTANCE:
            self.platforms.pop(0)
            if self.coins:
                self.coins.pop(0)

    def handle_portal_collision(self):
        if self.distance(self.player.position, self.portal.position) < self.portal.collision_radius:
            self.transition_active = True
            self.transition_time = 0.0
            self.difficulty += 1
            self.change_theme()
            
            # Son platformun pozisyonunu al
            last_platform = self.platforms[-1]
            plat_x, plat_y, plat_z = last_platform['pos']
            
            # Portalın olduğu yeri hesapla (Ortada olacak)
            portal_x = plat_x
            portal_y = plat_y + 1.5  # Biraz yüksekte
            portal_z = plat_z + 30  # 30 birimi ileriye taşıyoruz, isteğe göre ayarlanabilir
            
            # Önce portal öncesi 3 platform oluşturuyoruz
            prev_direction = 'forward'
            prev_x = plat_x
            prev_z = plat_z
            
            # Portal öncesindeki 3 platform
            for _ in range(3):
                platform, coin, prev_direction, prev_x, prev_z = self.generate_platform(prev_direction, prev_x, prev_z)
                self.platforms.append(platform)
                self.coins.append(coin)
            
            # Şimdi portalı oluştur
            self.portal = Portal(portal_x, portal_y, portal_z)
            
            # Sonra portal sonrasındaki 3 platformu oluşturuyoruz
            for _ in range(3):
                platform, coin, prev_direction, prev_x, prev_z = self.generate_platform(prev_direction, prev_x, prev_z)
                self.platforms.append(platform)
                self.coins.append(coin)

    def change_theme(self):
        self.current_theme = (self.current_theme + 1) % len(self.themes)
        if self.portal:
            self.portal.color = self.themes[self.current_theme].portal_color

    def update_physics(self, keys):
        if self.game_over:
            return
        current_platform = None
        for platform in self.platforms:
            px, py, pz = platform['pos']
            size = platform['size']
            if abs(self.player.position[0] - px) <= size/2 and abs(self.player.position[2] - pz) <= size/2:
                current_platform = platform
                break
        if keys[K_LEFT]:
            self.player.position[0] -= self.move_speed
        if keys[K_RIGHT]:
            self.player.position[0] += self.move_speed
        if keys[K_UP]:
            self.player.position[2] -= self.move_speed
        if keys[K_SPACE] and not self.player.is_jumping:
            self.player.velocity[1] = self.jump_power
            self.player.is_jumping = True
        self.player.velocity[1] -= self.gravity
        self.player.position[1] += self.player.velocity[1]
        on_platform = False
        for platform in self.platforms:
            if self.check_platform_collision(platform):
                on_platform = True
                break
        if not on_platform:
            self.player.is_jumping = True
        for coin in self.coins[:]:
            if self.distance(self.player.position, coin.position) < 1.0:
                self.coins.remove(coin)
                self.score += 10
                if self.score > self.high_score:
                    self.high_score = self.score
                    save_high_score(self.high_score)
        self.handle_portal_collision()
        self.update_platforms(self.player.position[2])
        if self.player.position[1] < -10:
            self.game_over = True

    def render(self):
        if self.game_over:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            draw_game_over(self.go_tex_id, self.go_tex_w, self.go_tex_h, self.textures, self.digit_textures, self.score, self.high_score, WINDOW_WIDTH, WINDOW_HEIGHT)
            pygame.display.flip()
            return
        if self.transition_active:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 1000.0)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            px, py, pz = self.player.position
            gluLookAt(
                px, py + 5, pz + 10,
                px, py, pz - 10,
                0, 1, 0
            )
            self.transition_time += 1.0 / FPS
            zoom = 1.0 + 8.0 * min(self.transition_time / self.transition_max, 1.0)
            if self.portal:
                self.portal.draw(animating=True, anim_time=self.transition_time, zoom=zoom)
            if self.transition_time >= self.transition_max:
                self.difficulty += 1
                self.change_theme()
                last_platform = self.platforms[-1]
                plat_x, plat_y, plat_z = last_platform['pos']
                self.portal = Portal(plat_x, plat_y + 1.5, plat_z)
                self.transition_active = False
                self.transition_time = 0.0
            pygame.display.flip()
            return
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        px, py, pz = self.player.position
        gluLookAt(
            px, py + 5, pz + 10,
            px, py, pz - 10,
            0, 1, 0
        )
        current_theme = self.themes[self.current_theme]
        glClearColor(*current_theme.sky_color)
        draw_skybox(self.textures['sky'][0])
        draw_platforms(self.platforms, self.portal.position, self.current_theme, self.themes[self.current_theme].platform_textures)
        for coin in self.coins:
            if coin.position[2] < self.portal.position[2]:
                continue
            coin.draw(self)
        if self.portal:
            self.portal.draw(animating=False, anim_time=0.0)
        self.player.draw()
        # Skor çizimi
        draw_score(self.score, self.high_score, self.digit_textures, WINDOW_WIDTH, WINDOW_HEIGHT)
        # Fade efekti
        if self.fade_alpha > 0:
            draw_fade(self.fade_alpha, WINDOW_WIDTH, WINDOW_HEIGHT)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
            keys = pygame.key.get_pressed()
            self.update_physics(keys)
            self.render()
            clock.tick(FPS)

   

    def distance(self, a, b):
        return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))

    def check_platform_collision(self, platform):
        x, y, z = platform['pos']
        s = platform['size']
        px, py, pz = self.player.position
        half_size = s / 2
        if (abs(px - x) < half_size and abs(pz - z) < half_size):
            platform_top = y + 1.5
            if (py - self.player.radius <= platform_top and py >= y and self.player.velocity[1] <= 0):
                self.player.position[1] = platform_top + self.player.radius
                self.player.velocity[1] = 0
                self.player.is_jumping = False
                return True
        return False

    def generate_initial_platforms(self):
        prev_direction = 'forward'
        prev_x = 0
        prev_z = 0
        for i in range(20):
            platform, coin, prev_direction, prev_x, prev_z = self.generate_platform(prev_direction, prev_x, prev_z)
            self.platforms.append(platform)
            self.coins.append(coin)
        last_platform = self.platforms[-1]
        plat_x, plat_y, plat_z = last_platform['pos']
        self.portal = Portal(plat_x, plat_y + 1.5, plat_z)

    def load_game_over_texture(self):
        try:
            surface = pygame.image.load('assets/textures/go.png').convert_alpha()
        except FileNotFoundError:
            surface = pygame.Surface((400, 200), pygame.SRCALPHA)
            font = pygame.font.Font(None, 72)
            text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text.get_rect(center=(200, 100))
            surface.blit(text, text_rect)
        texture_data = pygame.image.tostring(surface, "RGBA", 1)
        width, height = surface.get_width(), surface.get_height()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return tex_id, width, height

    def load_digit_textures(self):
        self.digit_textures = {}
        for i in range(10):
            path = f"assets/number textures/{i}.png"
            try:
                surface = pygame.image.load(path).convert_alpha()
                texture_data = pygame.image.tostring(surface, "RGBA", 1)
                width, height = surface.get_width(), surface.get_height()
                tex_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, tex_id)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                self.digit_textures[str(i)] = (tex_id, width, height)
            except Exception as e:
                print(f"{i}.png yüklenemedi: {e}")

if __name__ == "__main__":
    game = Game()
    game.run()


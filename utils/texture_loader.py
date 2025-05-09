import pygame
from OpenGL.GL import *

def load_texture(filename):
    try:
        # Pygame ile texture'ı yükle
        surface = pygame.image.load(filename)
        
        # RGBA formatına dönüştür
        image_data = pygame.image.tostring(surface, 'RGBA', True)
        width, height = surface.get_size()
        
        # OpenGL texture oluştur
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        # Texture parametrelerini ayarla
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        # Texture verisini yükle
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        
        return texture_id
    except Exception as e:
        print(f"Texture yükleme hatası ({filename}): {str(e)}")
        return None

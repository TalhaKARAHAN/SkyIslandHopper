import pygame
from OpenGL.GL import *

def load_texture(path):
    try:
        surface = pygame.image.load(path).convert_alpha()
        texture_data = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height()
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return texture_id, width, height
    except Exception as e:
        print(f"Texture yüklenirken hata: {path} - {str(e)}")
        return create_default_texture()

def create_default_texture():
    # Varsayılan texture oluştur (gri kare)
    texture_data = []
    for i in range(64):
        for j in range(64):
            texture_data.extend([128, 128, 128, 255])  # RGBA
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 64, 64, 0, GL_RGBA, GL_UNSIGNED_BYTE, bytes(texture_data))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    return texture_id, 64, 64

from PIL import Image
import os

def create_texture(name, color, size=(256, 256)):
    # Yeni bir resim oluştur
    img = Image.new('RGB', size, color)
    
    # textures klasörünü oluştur
    if not os.path.exists('textures'):
        os.makedirs('textures')
    
    # Resmi kaydet
    img.save(f'textures/{name}.jpg')

# Texture'ları oluştur
create_texture('grass', (34, 139, 34))  # Koyu yeşil
create_texture('ice', (173, 216, 230))  # Açık mavi
create_texture('sky', (135, 206, 235))  # Gökyüzü mavisi

print("Texture'lar oluşturuldu!") 
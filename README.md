SkyIslandHopper/
├── game.py # Ana oyun dosyası (çalıştırılabilir)
├── draw/ # Tüm çizim (render) fonksiyonları
│ ├── init.py
│ ├── cube.py
│ ├── skybox.py
│ ├── score.py
│ ├── platform.py
│ ├── game_over.py
│ └── fade.py
├── objects/ # Oyun nesneleri (oyuncu, coin, portal)
│ ├── player.py
│ ├── coin.py
│ └── portal.py
├── utils/ # Yardımcı modüller
│ ├── score.py
│ └── texture_loader.py
├── assets/ # Oyun varlıkları (görseller, dokular)
│ ├── textures/
│ └── number textures/
├── highscore.json # Yüksek skorun saklandığı dosya
├── requirements.txt
└── README.md


## Ana Python Dosyalarının İşlevleri

### game.py
- Oyun döngüsünü, ana pencereyi ve tüm oyun akışını yönetir.
- Oyun başlatma, skor, platform, coin ve portal yönetimi, sahne çizimi ve kullanıcı etkileşimi burada gerçekleşir.

### draw/ (Çizim Fonksiyonları)
- **cube.py:** Basit ve dokulu küp çizimi için fonksiyonlar.
- **skybox.py:** Skybox (gökyüzü küpü) çizimi.
- **score.py:** Skor ve rakam görselleriyle skor çizimi.
- **platform.py:** Platformların 3D olarak çizilmesi.
- **game_over.py:** Oyun bitti ekranı ve skorların görsel olarak gösterimi.
- **fade.py:** Ekran karartma (fade) efekti.
- **__init__.py:** Tüm çizim fonksiyonlarını dışa aktarır.

### objects/ (Oyun Nesneleri)
- **player.py:** Oyuncu karakterinin hareketi, çizimi ve fiziksel özellikleri.
- **coin.py:** Coin nesnesinin konumu, animasyonu ve çizimi.
- **portal.py:** Portal nesnesinin konumu, animasyonu ve çizimi.

### utils/ (Yardımcı Modüller)
- **score.py:** Yüksek skorun dosyada saklanması ve okunması.
- **texture_loader.py:** Doku (texture) dosyalarını yükleme ve varsayılan doku oluşturma.

### assets/
- **textures/**: Oyun içi platform, coin, skybox, skor gibi tüm görsel dokular.
- **number textures/**: Skor ve sayı göstergeleri için rakam görselleri (0-9).

## Oyun Kontrolleri

- Yön tuşları veya W/A/D: Hareket
- SPACE: Zıplama
- R: Oyun bittiğinde yeniden başlat
- ESC: Oyundan çıkış

## Oyun Mekanikleri

- Coin toplayarak skorunu artır.
- Platformlar arasında düşmeden ilerle.
- Portaldan geçerek yeni temaya/evrene geç.
- Yüksek skorun kaydedilir ve oyun sonunda gösterilir.

## Lisans

MIT Lisansı - Ayrıntılar için LICENSE dosyasına bakınız.

---

## Notlar

- Tüm çizim fonksiyonları `draw/` klasöründe modüler olarak tutulur.
- Oyun nesneleri ve yardımcı fonksiyonlar ilgili klasörlerde tek sorumluluk prensibiyle ayrılmıştır.
- Oyun, `python game.py` komutuyla başlatılır.

---

Her bir `.py` dosyasının işlevi ve projenin genel yapısı bu şekildedir.  
Daha fazla açıklama veya örnek kod istersen, detaylandırabilirim!
class Brick(pg.sprite.Sprite):  # inherit from sprite

    def __init__(self, color):
        super().__init__()
        width = 70
        height = 80
        self.image = pygame.image.load('astro_shield.png')
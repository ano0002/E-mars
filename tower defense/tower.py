import pygame

class Turret(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class PlaceHolder(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(255,255,0)):
        super().__init__()
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

if __name__ == "__main__":
    from terrain import Terrain
    pygame.init()
    pygame.display.set_caption("Terrain")
    display = pygame.display.set_mode((800, 600))
    terrain = Terrain("./tiled_map/map.csv")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.fill((0,0,0))
        terrain.draw(display)
        pygame.display.update()
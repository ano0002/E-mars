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
    buttons = pygame.sprite.Group()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                        for button in buttons:
                            if button.rect.collidepoint(event.pos):
                                button.on_click(button,mousepos=event.pos)
        display.fill((0,0,0))
        terrain.draw(display)
        buttons.update(pygame.mouse.get_pos())
        buttons.draw(display)
        pygame.display.update()
import pygame

class Turret(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class PlaceHolder(pygame.sprite.Sprite):
    def __init__(self, x, y,terrain):
        super().__init__()
        self.image = pygame.Surface([16,16], pygame.SRCALPHA)
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.terrain = terrain
    
    def update(self, mousepos):
        self.rect.center = mousepos
        for tile in self.terrain.placing_tiles:
            if tile.rect.collidepoint(mousepos):
                self.rect.center = tile.rect.center
                self.image.fill((0,80,0))
                break
    
    def draw(self, display):
        display.blit(self.image, self.rect)
if __name__ == "__main__":
    from terrain import Terrain
    from ui import Button
    pygame.init()
    pygame.display.set_caption("Terrain")
    display = pygame.display.set_mode((800, 600))
    terrain = Terrain("./tiled_map/map.csv")
    turrets = pygame.sprite.Group()
    placeholder = None
    def new_turret(button, mousepos):
        global placeholder
        """
        turret = Turret(0,0, "./assets/tower.png")
        turrets.add(turret)
        """
        placeholder = PlaceHolder(*mousepos,terrain)
        
    buttons = pygame.sprite.Group(Button(512,0,100,50,text="Test",on_click=new_turret))
    
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
        turrets.draw(display)
        if placeholder : 
            placeholder.update(pygame.mouse.get_pos())
            placeholder.draw(display)
            
        pygame.display.update()
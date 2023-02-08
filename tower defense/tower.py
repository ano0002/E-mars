import pygame
from ui import Button

class Turret(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.selected = False
        self.on_click = self.select
    
    def select(self, button, mousepos):
        self.selected = not self.selected
        for turret in turrets:
            if turret != self:
                turret.selected = False
    

class LaserTurret(Turret):
    damage = 10
    range = 50
    fire_rate = 0.5
    cost = 100
    def __init__(self, x, y):
        super().__init__(x, y, "./assets/tower.png")

class PlaceHolder(Button):
    def __init__(self, x, y,terrain,turret_type):
        super().__init__(x,y,16,16,(0,255,0),on_click=self.on_click)
        self.terrain = terrain
        self.turret_type = turret_type
        self.range_image = pygame.Surface((self.turret_type.range*2,self.turret_type.range*2),pygame.SRCALPHA)
        pygame.draw.circle(self.range_image,(0,0,0,100),(self.turret_type.range,self.turret_type.range),self.turret_type.range)
        self.range_rect = self.range_image.get_rect()
            
    def update(self, mousepos):
        self.rect.center = mousepos
        self.image.fill((255,0,0))
        for tile in self.terrain.placing_tiles:
            if tile.rect.collidepoint(mousepos):
                self.rect.center = tile.rect.center
                self.image.fill((0,80,0))
                break
        self.range_rect.center = self.rect.center
    
    def draw(self, display):
        display.blit(self.range_image, self.range_rect)
        display.blit(self.image, self.rect)
        
    
    def on_click(self,button,mousepos):
        if self.image.get_at((0,0)) == (0,80,0):
            turret = self.turret_type(*self.rect.center)
            turrets.add(turret)
            self.kill()
    
    def kill(self):
        global placeholder
        buttons.remove(self)
        placeholder = None
        del self
    
if __name__ == "__main__":
    from terrain import Terrain
    pygame.init()
    pygame.display.set_caption("Turrets")
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
        placeholder = PlaceHolder(*mousepos,terrain,LaserTurret)
        buttons.add(placeholder)
        
    buttons = pygame.sprite.Group(Button(512,0,100,50,text="Test",on_click=new_turret))
    
    def unselect_all():
        for turret in turrets:
            turret.selected = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                        unselect = True
                        for button in buttons:
                            if button.rect.collidepoint(event.pos):
                                button.on_click(button,mousepos=event.pos)
                                unselect = False
                        for turret in turrets:
                            if turret.rect.collidepoint(event.pos):
                                turret.on_click(turret,mousepos=event.pos)
                                unselect = False
                        if unselect:
                            unselect_all()
        display.fill((0,0,0))
        terrain.draw(display)
        buttons.update(pygame.mouse.get_pos())
        buttons.draw(display)
        turrets.update(pygame.mouse.get_pos())
        turrets.draw(display)
        
        for turret in turrets:
            if turret.selected:
                pygame.draw.circle(display, (255,0,0), turret.rect.center, turret.range, 1)
        
        if placeholder : 
            placeholder.update(pygame.mouse.get_pos())
            placeholder.draw(display)
            
        pygame.display.update()
import pygame,random
from particle import Particle
from custom_maths import x_y_components
import __main__
from pygame.math import Vector2

class Ennemy(pygame.sprite.Sprite):
    def __init__(self, pos,direction,terrain, color = (255,0,0), radius = 8,pv = 1):
        global game
        super().__init__()
        self.pos = pos
        self.direction = direction
        self.color = color
        self.radius = radius
        self.particles = []
        self.frame = random.randint(0,16)
        self.image = pygame.Surface((radius*2,radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius,radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.alive = True
        self.pv = pv
        self.terrain = terrain
        self.progress = 0
        if hasattr(__main__,'game'):
            __main__.game.ennemies.add(self)
        
    def update(self):
        if self.alive :
            if self.direction == 1:
                self.pos[0] += 1
            elif self.direction == 3:
                self.pos[0] -= 1
            elif self.direction == 4:
                self.pos[1] -= 1
            elif self.direction == 2:
                self.pos[1] += 1
            self.rect.center = self.pos
            
            terrain_px_width = len(self.terrain.tiles[0])*self.terrain.width
            terrain_px_height = len(self.terrain.tiles)*self.terrain.height
            if self.pos[0] > terrain_px_width or self.pos[1] > terrain_px_height or self.pos[1] < 0:
                self.alive = False
                if hasattr(__main__,'game'):
                    __main__.game.hit(self.pv)
                super().kill()
                            
            if self.pos[0]>0 :
                self.progress += 0.1
                if self.direction%2 == 0:
                    if (self.pos[1]-8) % 16 == 0:
                        self.direction = self.terrain.get_direction(self.pos)
                else:
                    if (self.pos[0]-8) % 16 == 0:
                        self.direction = self.terrain.get_direction(self.pos)
            self.frame += 1
    
    def hit(self, damage):
        self.pv -= damage
        if self.pv != float('inf'):
            if hasattr(__main__,'game'):
                __main__.game.money += damage
        if self.pv <= 0:
            self.kill()
    
    def kill(self) -> None:
        if hasattr(__main__,'game'):
            __main__.game.ennemies.remove(self)
            for i in range(5):
                __main__.game.particles.append(
                    Particle(list(self.pos), Vector2(x_y_components(i*360/5,random.random())),20, (255,0,0), 2, 0))
        self.alive = False
        super().kill()
               
    
    @property
    def alive(self) -> bool:
        return self._alive
    
    @alive.setter
    def alive(self, value: bool) -> None:
        self._alive = value
    
    def __repr__ (self):
        return "Ennemy at "+str(self.pos)
            

class EnnemyManager():
    def __init__(self, map, waves=[]):
        self.map = map
        self.rounds = waves
        self.round = 0

    def next_wave(self):
        for wave in self.rounds[self.round]:
            wave.spawning = True
        self.round += 1

    def draw(self, display):
        for waves in self.rounds:
            for wave in waves:
                wave.ennemies.draw(display)

    def update(self):
        for waves in self.rounds:
            for wave in waves:
                wave.update()
        
    def add_round(self,round):
        self.rounds.append(round)

class Wave():
    def __init__(self,number ,timing, life, speed, damage, color,tilemap):
        self.number = number
        self.timing = timing
        self.map = tilemap
        self.life = life
        self.speed = speed
        self.damage = damage
        self.color = color
        self.ennemies = pygame.sprite.Group()
        self.spawning = False
        self.frame = 0
        
    def update(self):
        self.frame += 1
        if self.spawning:
            if self.frame % self.timing == 0:
                self.ennemies.add(Ennemy([-16,24], 1,self.map,self.color,pv=self.life))
                self.number -= 1
            if self.number == 0:
                self.spawning = False
                self.frame = 0
        self.ennemies.update()
    
    

if __name__ == "__main__":
    import terrain
    from ui import Button
    
    pygame.init()
    clock = pygame.time.Clock()
    terrain = terrain.Terrain("./tiled_map/map.csv")
    spawner = EnnemyManager(terrain,[[Wave(10,16,1,1,1,(255,0,0),terrain)]])
    
    def new_wave(button, mousepos):
        print("New wave")
        spawner.next_wave()
        
    buttons = pygame.sprite.Group(Button(512,0,200,50,text="Start Wave",on_click=new_wave))
    
    display = pygame.display.set_mode((800,600))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                        unselect = True
                        for button in buttons:
                            if button.rect.collidepoint(event.pos):
                                button.on_click(button,mousepos=event.pos)
                                unselect = False
        display.fill((0,0,0))
        terrain.draw(display)
        spawner.update()
        spawner.draw(display)
        buttons.update(pygame.mouse.get_pos())
        buttons.draw(display)
        pygame.display.flip()
        clock.tick(60)
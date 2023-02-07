import pygame,random

class Ennemy(pygame.sprite.Sprite):
    def __init__(self, pos,direction,terrain, color = (255,0,0), radius = 8,pv = 1):
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
                del self
                return
                self.game.hit(self.pv)
            
            if self.pos[0]>0 :
                if self.direction%2 == 0:
                    if (self.pos[1]-8) % 16 == 0:
                        self.direction = self.terrain.get_direction(self.pos)
                else:
                    if (self.pos[0]-8) % 16 == 0:
                        self.direction = self.terrain.get_direction(self.pos)
            self.frame += 1
    
    def hit(self, damage):
        self.pv -= damage
        if self.pv <= 0:
            self.alive = False
            

class EnnemyManager():
    def __init__(self, map, waves):
        self.map = map
        self.waves = waves
        self.wave = 0
        self.next_wave()

    def next_wave(self):
        self.waves[self.wave].spawning = True
        self.wave += 1

    def draw(self, display):
        for wave in self.waves:
            wave.ennemies.draw(display)

    def update(self):
        for wave in self.waves:
            wave.update()

class Wave():
    def __init__(self,number ,timing, life, speed, damage, color,tilemap):
        self.number = number-1
        self.timing = timing
        self.map = tilemap
        self.life = life
        self.speed = speed
        self.damage = damage
        self.color = color
        self.ennemies = pygame.sprite.Group(Ennemy([-16,24], 1,self.map))
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
    
    pygame.init()
    clock = pygame.time.Clock()
    terrain = terrain.Terrain("./tiled_map/map.csv")
    spawner = EnnemyManager(terrain,[Wave(10,16,1,1,1,(255,0,0),terrain)])
    
    display = pygame.display.set_mode((800,600))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        display.fill((0,0,0))
        terrain.draw(display)
        spawner.update()
        spawner.draw(display)
        pygame.display.flip()
        clock.tick(60)
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
        if self.direction == 1:
            self.pos[0] += 1
        elif self.direction == 3:
            self.pos[0] -= 1
        elif self.direction == 4:
            self.pos[1] -= 1
        elif self.direction == 2:
            self.pos[1] += 1
        self.rect.center = self.pos
        if (self.pos[1]-7) % 16 == 0 or (self.pos[0]-7) % 16 == 0:
            self.direction = self.terrain.get_direction(self.pos)
        self.frame += 1
    
    def hit(self, damage):
        self.pv -= damage
        if self.pv <= 0:
            self.alive = False
            

class EnnemyManager():
    def __init__(self, map, waves):
        self.map = map
        self.ennemies = pygame.sprite.Group()
        self.waves = waves
        self.next_wave()

    def next_wave(self):
        for i in range(10):
            self.ennemies.add(Ennemy([i*16,24], 1,self.map))

    def draw(self, display):
        self.ennemies.draw(display)

    def update(self):
        self.ennemies.update()

if __name__ == "__main__":
    import terrain
    
    pygame.init()
    clock = pygame.time.Clock()
    terrain = terrain.Terrain("./tiled_map/map.csv")
    spawner = EnnemyManager(terrain)
    
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
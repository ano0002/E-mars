import pygame

class Tileset:
    def __init__(self, file, tilesize=(16, 16)):
        self.file = file
        self.size = tilesize
        self.width = self.size[0]
        self.height = self.size[1]
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        
        self.tiles = []
        self.load()
    
    def load(self):
        w = self.rect.width//self.width
        h = self.rect.height//self.height
        for i in range(h):
            for j in range(w):
                tile = pygame.Surface(self.size, pygame.SRCALPHA)
                tile.blit(self.image, (0, 0), (j*self.width, i*self.height, *self.size))
                self.tiles.append(tile)

class MovementTile(pygame.sprite.Sprite):
    def __init__(self, x, y,direction, width, height, color=(255,255,0)):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        
class PlacingTerrain(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(0,255,0)):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Terrain(pygame.sprite.Group):
    def __init__(self, file, tilesize=(16, 16)):
        super().__init__()
        self.file = file
        self.size = tilesize
        self.width = self.size[0]
        self.height = self.size[1]
        
        self.placing_tiles = pygame.sprite.Group()
        self.move_tiles = pygame.sprite.Group()
        
        self.tiles = []
        self.load()
        self.gun = "test"

    def load(self):
        with open(self.file, 'r') as f:
            for y,line in enumerate(f):
                temp = []
                for x,item in enumerate(line.strip().split(",")) :
                    item = int(item)
                    if item == 0:
                        tile = PlacingTerrain(x*self.width, y*self.height, self.width, self.height)
                        self.placing_tiles.add(tile)
                    else:
                        tile = MovementTile(x*self.width, y*self.height, item, self.width, self.height)
                        self.move_tiles.add(tile)
                    self.add(tile)
                    temp.append(tile)
                self.tiles.append(temp)

    def get_direction(self, pos):
        x,y = pos
        x/= self.width
        y /= self.height
        return self.tiles[int(y)][int(x)].direction

if __name__ == "__main__":
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
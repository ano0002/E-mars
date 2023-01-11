import pygame
import numpy as np

class Map:
    def __init__(self, map_file):
        self.map_file = map_file
        self.map = []
        self.load_map()
    
    def load_map(self):
        with open(self.map_file, 'r') as f:
            for line in f:
                self.map.append([int(l) for l in line.split(",")])
        
        
    def show_map(self):
        for line in self.map:
            print(line)

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def blit(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

class Tileset:
    def __init__(self, file, size=(16, 16), margin=0, spacing=0):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()


    def load(self):

        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing
        
        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'
    
class Tilemap:
    def __init__(self, tileset,map_file, size=(20, 30), rect=None):
        self.size = size
        self.tileset = tileset
        self.map_file = map_file
        self.load_map()
        h, w = self.size
        self.image = pygame.Surface((16*w, 16*h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def load_map(self):
        self.map = []
        with open(self.map_file, 'r') as f:
            for line in f:
                self.map.append([int(l) for l in line.split(",")])
                
    def render(self):
        m, n = self.size
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i][j]]
                self.image.blit(tile, (j*16, i*16))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        print(self.map)
        print(self.map.shape)
        self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        print(self.map)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'
    
if __name__ == '__main__':
    pygame.init()
    display_width = 20*16
    display_height = 30*16
    display = pygame.display.set_mode((display_width, display_height))
    tileset = Tileset('terrain.png')
    tilemap = Tilemap(tileset,'map.csv')
    tilemap.render()
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
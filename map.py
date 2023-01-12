import pygame
import numpy as np

class Tileset:
    def __init__(self, file, tilesize=(16, 16)):
        self.file = file
        self.size = tilesize
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()
    
    def load(self):
        w = self.rect.width//self.size[0]
        h = self.rect.height//self.size[1]
        for i in range(h):
            for j in range(w):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (j*self.size[0], i*self.size[1], *self.size))
                self.tiles.append(tile)

class Map:
    def __init__(self, map_file, tileset):
        self.map_file = map_file
        self.map = []
        self.load_map()
        self.tileset = tileset
    
    def load_map(self):
        with open(self.map_file, 'r') as f:
            for line in f:
                self.map.append([int(l) for l in line.split(",")])
    def show_map(self,display):
        for i,line in enumerate(self.map):
            for j,item in enumerate(line):
                display.blit(self.tileset.tiles[item], (j*16, i*16))
    
if __name__ == '__main__':
    pygame.init()
    display_width = 20*16
    display_height = 30*16
    display = pygame.display.set_mode((display_width, display_height))
    tileset = Tileset('terrain.png')
    playing_area = Map('map.csv', tileset)
    playing_area.show_map(display)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
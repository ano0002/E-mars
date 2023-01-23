import pygame
from pygame.math import Vector2

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
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (j*self.width, i*self.height, *self.size))
                self.tiles.append(tile)

class Map:
    def __init__(self, map_file, tileset,offset=[0,0],size=(60,40)):
        self.map_file = map_file
        self.map = []
        self.load_map()
        self.tileset = tileset
        self.offset = offset
        self.width = size[0]
        self.height = size[1]
    def load_map(self):
        with open(self.map_file+"_Background.csv", 'r') as back:
            with open(self.map_file+"_Platforms.csv", 'r') as platforms:
                for line in platforms:
                    backline =  [int(l) for l in back.readline().split(",")]
                    temp = [int(l) for l in line.split(",")]
                    for index,elem in enumerate(temp):
                        if elem == -1:
                            temp[index] = backline[index]
                    self.map.append(temp)
                
    def show_map(self,display):
        display_tile_width = display.get_rect().width // self.tileset.width
        display_tile_height = display.get_rect().height // self.tileset.height
        for i,line in enumerate(self.map[self.offset[1]:self.offset[1]+display_tile_height]):
            for j,item in enumerate(line[self.offset[0]:self.offset[0]+display_tile_width]):
                display.blit(self.tileset.tiles[item], (j*self.tileset.width, i*self.tileset.height))
    
    def get_colliders(self,display):
        colliders = []
        display_tile_width = display.get_rect().width // self.tileset.width
        display_tile_height = display.get_rect().height // self.tileset.height
        for i,line in enumerate(self.map[self.offset[1]:self.offset[1]+display_tile_height]):
            for j,item in enumerate(line[self.offset[0]:self.offset[0]+display_tile_width]):
                if item not in (111,23,66,29,117):
                    colliders.append(pygame.Rect(j*self.tileset.width, i*self.tileset.height, self.tileset.width, self.tileset.height))
        return colliders
    
    def get_interactibles(self,display):
        interactibles = []
        display_tile_width = display.get_rect().width // self.tileset.width
        display_tile_height = display.get_rect().height // self.tileset.height
        for i,line in enumerate(self.map[self.offset[1]:self.offset[1]+display_tile_height]):
            for j,item in enumerate(line[self.offset[0]:self.offset[0]+display_tile_width]):
                if item in (181,203,225):
                    interactibles.append(pygame.Rect(j*self.tileset.width, i*self.tileset.height, self.tileset.width, self.tileset.height))
        return interactibles

    def interact(self,rect,player,display):
        pass
    
    def shot(self,rect,player,display):
        pos = list(map(int,Vector2(rect.center)//16))
        print(pos)
        if self.map[pos[1]+self.offset[1]][pos[0]+self.offset[0]] in (181,203,225):
            self.map[pos[1]+self.offset[1]][pos[0]+self.offset[0]] = 111


if __name__ == '__main__':
    pygame.init()
    tileset = Tileset('./tiled_map/terrain.png')
    playing_area = Map('./tiled_map/map', tileset,offset=[0,0], size=[80,45])
    display_width = playing_area.width*16
    display_height = playing_area.height*16
    display = pygame.display.set_mode((display_width, display_height))
    playing_area.show_map(display)
    for collider in playing_area.get_colliders(display):
        pygame.draw.rect(display, (255, 0, 0), collider, 1)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    playing_area.offset[1] -= playing_area.height
                if event.key == pygame.K_DOWN:
                    playing_area.offset[1] += playing_area.height
        playing_area.show_map(display)
        for collider in playing_area.get_colliders(display):
            pygame.draw.rect(display, (255, 0, 0), collider, 1)
        for collider in playing_area.get_interactibles(display):
            pygame.draw.rect(display, (0, 0, 255), collider, 1)
        pygame.display.update()
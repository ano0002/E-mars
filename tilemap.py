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
                tile = pygame.Surface(self.size, pygame.SRCALPHA)
                tile.blit(self.image, (0, 0), (j*self.width, i*self.height, *self.size))
                self.tiles.append(tile)

class Map:
    def __init__(self, map_file, tileset,offset=[0,0],size=(60,40)):
        self.map_file = map_file
        self.map = []
        self.load_map()
        self.tileset = tileset
        self._offset = offset
        self.width = size[0]
        self.height = size[1]
        self.frame = 0
        
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
                
        
    @property
    def offset(self):
        return self._offset
    
    @offset.setter
    def offset(self,offset):
        offset[1] = max(0,offset[1])
        
        offset[1] = min(offset[1],len(self.map)-self.height)
        
        if not isinstance(offset, Vector2):
            self._offset = Vector2(offset)
        else :
            self._offset = offset            
    
    def show_map(self,display):
        self.frame += 1
        display_tile_width = display.get_rect().width // self.tileset.width
        display_tile_height = display.get_rect().height // self.tileset.height
        bottom = round(self.offset[1]+0.5)+display_tile_height
        top = int(self.offset[1])
        right = round(self.offset[0]+0.5)+display_tile_width
        left = int(self.offset[0])
        y_offset = self.offset[1]%1*self.tileset.height
        x_offset = self.offset[0]%1*self.tileset.height
        collectibles = []
        for i,line in enumerate(self.map[top:bottom]):
            for j,item in enumerate(line[left:right]):
                if item  ==  67:                    
                    display.blit(self.tileset.tiles[23], (j*self.tileset.width+x_offset, i*self.tileset.height-y_offset))
                    collectibles.append({"pos":(j*self.tileset.width,i*self.tileset.height),"tile":self.tileset.tiles[67]})
                else:
                    display.blit(self.tileset.tiles[item],
                                 (j*self.tileset.width+x_offset,i*self.tileset.height-y_offset))
        for collectible in collectibles:
            effect= abs(self.frame%90-45)*0.15
            display.blit(pygame.transform.scale(collectible["tile"],(32,32)), (collectible["pos"][0]+x_offset-self.tileset.height/2, collectible["pos"][1]-y_offset-self.tileset.height+effect))
    
    def get_colliders(self,display):
        colliders = []
        display_tile_width = display.get_rect().width // self.tileset.width
        display_tile_height = display.get_rect().height // self.tileset.height
        bottom = round(self.offset[1]+display_tile_height+0.5)
        top = int(self.offset[1])
        right = round(self.offset[0]+display_tile_width+0.5)
        left = int(self.offset[0])
        y_offset = self.offset[1]%1*self.tileset.height
        x_offset = self.offset[0]%1*self.tileset.height
        for i,line in enumerate(self.map[top:bottom]):
            for j,item in enumerate(line[left:right]):
                if item not in (111,23,66,29,117,67,205):
                    colliders.append(pygame.Rect(j*self.tileset.width-x_offset, i*self.tileset.height-y_offset, self.tileset.width, self.tileset.height))
        return colliders
    
    
    def get_interactibles(self,display):
        interactibles = {"rects":[],"tiles":[]}
        display_tile_width = display.get_rect().width // self.tileset.width
        display_tile_height = display.get_rect().height // self.tileset.height
        bottom = round(self.offset[1]+display_tile_height+0.5)
        top = int(self.offset[1])
        right = round(self.offset[0]+display_tile_width+0.5)
        left = int(self.offset[0])
        y_offset = self.offset[1]%1*self.tileset.height
        x_offset = self.offset[0]%1*self.tileset.height
        for i,line in enumerate(self.map[top:bottom]):
            for j,item in enumerate(line[left:right]):
                if item in (181,203,225,67):
                    interactibles["rects"].append(pygame.Rect(j*self.tileset.width-x_offset, i*self.tileset.height-y_offset, self.tileset.width, self.tileset.height))
                    interactibles["tiles"].append(item)
        return interactibles

    def interact(self,rect,tile,player,display):
        y_offset = self.offset[1]%1*self.tileset.height
        x_offset = self.offset[0]%1*self.tileset.height
        pos = list(map(int,Vector2(rect.centerx+x_offset,rect.centery+y_offset)//16))
        if self.map[pos[1]+int(self.offset[1])][pos[0]+int(self.offset[0])] in (67,0):
            if player :
                player.power =15
                player.gun = "assets/shotgun.png"
            self.map[pos[1]+int(self.offset[1])][pos[0]+int(self.offset[0])] = 111
            
    def shot(self,rect,tile,player,display):
        pos = list(map(int,Vector2(rect.center)//16))
        if self.map[pos[1]+int(self.offset[1])][pos[0]+int(self.offset[0])] in (181,203,225):
            self.map[pos[1]+int(self.offset[1])][pos[0]+int(self.offset[0])] = 111


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
    clock = pygame.time.Clock()
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    playing_area.offset -= Vector2(0,0.4)
                if event.key == pygame.K_DOWN:
                    playing_area.offset += Vector2(0,0.4)
            if event.type == pygame.MOUSEWHEEL:    
                playing_area.offset += Vector2(0,-event.y)
        playing_area.show_map(display)
        
        for collider in playing_area.get_colliders(display):
            pygame.draw.rect(display, (255, 0, 0), collider, 1)
        for collider in playing_area.get_interactibles(display)["rects"]:
            pygame.draw.rect(display, (0, 0, 255), collider, 1)
        
        pygame.display.update()
        
        clock.tick(60)
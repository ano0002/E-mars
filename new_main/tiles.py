import pygame
from particle import Torch


class TileSet(object):
    def __init__(self, filename, tile_size):
        self.tile_size = tile_size
        self.tiles = []
        self.load_tiles(filename)

    def load_tiles(self, filename):
        image = pygame.image.load(filename)
        image_width, image_height = image.get_size()
        for tile_y in range(0, image_height, self.tile_size):
            for tile_x in range(0, image_width, self.tile_size):
                rect = (tile_x, tile_y, self.tile_size, self.tile_size)
                self.tiles.append(image.subsurface(rect))

    def get_tile(self, tile_id):
        return self.tiles[tile_id]
    
    def get_tile_size(self):
        return self.tile_size

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, tileset, tile_id):
        super().__init__()
        self.pos = pos
        self.tileset = tileset
        self.id = tile_id
        self.tile_size = self.tileset.get_tile_size()
        self.default_pos = pos.copy()

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
        self.image = self.tileset.get_tile(value)
        self.rect = self.image.get_rect(top=self.pos[1], left=self.pos[0])
    
    @property
    def x(self):
        return self.pos[0]
    
    @x.setter
    def x(self, value):
        self.pos[0] = value
        self.rect.x = value
        
    @property
    def y(self):
        return self.pos[1]
    
    @y.setter
    def y(self, value):
        self.pos[1] = value
        self.rect.y = value
    
    def reset_pos(self):
        self.x = self.default_pos[0]
        self.y = self.default_pos[1]
        
    def draw(self, screen, frame= 0):
        if self.x < -self.tile_size \
            or self.x > screen.get_width() \
                or self.y < -self.tile_size \
                    or self.y > screen.get_height():
            return None
        if self.id != 67 : #Is not a moving item
            screen.blit(self.image, self.rect)
        else: #Is a moving item
            screen.blit(self.tileset.tiles[23],self.rect)
            #calculate the position of the moving item
            effect= abs(frame%30-15)*0.15
            transformed_image = pygame.transform.scale(self.image,(32,32))
            screen.blit(transformed_image, (self.x-self.tile_size/2, self.y-self.tile_size+effect))
    
    def __repr__(self) -> str:
        return super().__repr__() + f"({self.id})"

def id_to_tile(tile_id,x,y,tileset): 
    tile_size = tileset.get_tile_size()
    x *= tile_size
    y *= tile_size
    if tile_id != -1:
        return Tile([x,y], tileset, tile_id)
    else:
        return None 

class Tilemap():
    def __init__(self, filename, tile_set, offset=[0,0]):
        super().__init__()
        self.tile_set = tile_set
        self.tile_size = self.tile_set.get_tile_size()
        self._offset = offset
        self.torchs = []
        self.foreground = []
        self.background = []
        self.tiles = []
        self.load_tiles(filename)
        self.frame = 0

    def load_tiles(self, filename):
        self.width = 0
        self.height = 0
        with open(filename+"_Platforms.csv") as fore:
            for y,line in enumerate(fore):
                line = line.rstrip()
                if not line:
                    continue
                else:
                    line = line.split(",")
                    line = list(map(int,line))
                    for x,value in enumerate(line):
                        line.pop(x)
                        tile = id_to_tile(value,x,y,self.tile_set)
                        line.insert(x,tile)
                    self.tiles.append(line.copy())
                    self.foreground.append(line)
                    if len(line) > self.width:
                        self.width = len(line)
            
        with open(filename+"_Background.csv") as back:
            for y,line in enumerate(back):
                line = line.rstrip()
                if not line:
                    continue
                else:
                    line = line.split(",")
                    line = list(map(int,line))
                    for x,value in enumerate(line):
                        line.pop(x)
                        tile = id_to_tile(value,x,y,self.tile_set)
                        line.insert(x,tile)
                        if self.get_tile_by_map_coord(x,y) == None:
                            if value == 66:
                                torch_position = [(x+0.5)*self.tile_size,(y+0.5)*self.tile_size]
                                torch = Torch(torch_position,offset=self.offset)
                                self.torchs.append(torch)
                            self.tiles[y].pop(x)
                            self.tiles[y].insert(x,tile)
                    self.background.append(line)
                    
                    if len(line) > self.width:
                        self.width = len(line)
                    
        self.height = len(self.tiles)
    def draw(self, surface):
        self.frame += 1
        for line in self.foreground:
            for tile in line:
                if tile != None:
                    tile.draw(surface,self.frame)
                    
        for torch in self.torchs:
            torch.update(offset=self.offset)
            torch.draw(surface)
    
    def get_tile_size(self):
        return self.tile_set.get_tile_size()

    @property
    def offset(self):
        return self._offset
    
    @offset.setter
    def offset(self, value):
        for line in self.tiles:
            for tile in line:
                if tile != None:
                    tile.x = value[0]+tile.default_pos[0]
                    tile.y = value[1]+tile.default_pos[1]
                    
        self._offset = value
        
    def get_tile_by_screen_coord(self, x, y):
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return tile
            
        return None

    def get_tile_by_map_coord(self, x, y):
        return self.tiles[y][x]
    
    def get_tiles_of_type(self, tile_id):
        tiles = []
        for tile in self.tiles:
            if tile.id == tile_id:
                tiles.append(tile)
        return tiles

    def get_colliders(self):
        colliders = []
        for line in self.foreground:
            for tile in line:
                if tile != None:
                    if tile.id not in {66,67}:
                        colliders.append(tile.rect)
        return colliders

    def get_interactibles(self):
        interactibles = []
        for line in self.foreground:
            for tile in line:
                if tile != None:
                    if tile.id in {66,67}:
                        interactibles.append(tile)
        return interactibles

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)
    tile_set = TileSet(".\\tiled_map\\terrain.png", 16)
    tile_map = Tilemap(".\\tiled_map\\map", tile_set)
    running = True
    clock = pygame.time.Clock()
    print(tile_map.foreground)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                tile_map.offset = (tile_map.offset[0], tile_map.offset[1] + event.y*16)
        screen.fill((33,31,48))
        tile_map.draw(screen)
        pygame.display.flip()
        clock.tick(60)
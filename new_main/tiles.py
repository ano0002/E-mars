import pygame

class TileSet(object):
    def __init__(self, filename, tile_size):
        self.tile_size = tile_size
        self.tiles = []
        self.load_tiles(filename)

    def load_tiles(self, filename):
        image = pygame.image.load(filename)
        image_width, image_height = image.get_size()
        for tile_x in range(0, image_width, self.tile_size):
            line = []
            self.tiles.append(line)
            for tile_y in range(0, image_height, self.tile_size):
                rect = (tile_x, tile_y, self.tile_size, self.tile_size)
                line.append(image.subsurface(rect))

    def get_tile(self, x, y):
        return self.tiles[x][y]
    
    def get_tile_size(self):
        return self.tile_size

class Tile():
    def __init__(self, pos, tileset, tile_id):
        self.pos = pos
        self.tileset = tileset
        self.id = tile_id

class Tilemap(object):
    def __init__(self, filename, tile_size):
        self.tile_size = tile_size
        self.tiles = []
        self.load_tiles(filename)

    def load_tiles(self, filename):
        with open(filename) as f:
            for y,line in f:
                line = line.rstrip()
                if not line:
                    continue
                else:
                    for x,value in enumerate(map(line.split(','),int)):
                        tile = Tile((x,y), self.tileset, value)
                        self.tiles.append(tile)

    
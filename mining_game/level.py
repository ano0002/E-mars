import pygame 
from .tiles import Tile, Tileset, tile_size
from .loader import import_csv_layout

class Level:
    def __init__(self, path, surface):
        # general setup
        self.display_surface = surface
        terrain_layout = import_csv_layout(path)
        self.terrain_sprites = self.create_tile_group(terrain_layout)

    def create_tile_group(self, layout):
        sprite_group = pygame.sprite.Group()
        tileset = Tileset(16, 16, "./mining_game/bloc_pics/blocs_pic.png")   # 16, 16 is the size of 1 tile on the picture
        for row_index, row in enumerate(layout):
            #sprite_group.add(Tile((48, 48), -1, tileset))    # Add blank to sprite (at x = y = 48)
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = (col_index) * tile_size   # col_index + somethiing for offset
                    y = (row_index) * tile_size   # same here
                    sprite = Tile((x, y), val, tileset)
                    sprite_group.add(sprite)
        return sprite_group
    
    def run(self):
        self.terrain_sprites.draw(self.display_surface)
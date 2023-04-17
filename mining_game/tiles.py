import pygame 

tile_size = 65

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,index,tileset):
		super().__init__()
		self.image = tileset.tileset_list[index]
		self.rect = self.image.get_rect(topleft = pos)
		self.index = index

	def __repr__(self) -> str:
		return f"Tile({self.rect.x},{self.rect.y}) - {self.index}"


class Tileset:
	def __init__(self,tile_width,tile_height,path):
		self.tile_width = tile_width
		self.tile_height = tile_height
		self.tileset = pygame.image.load(path).convert_alpha()
		self.generate_tileset()

	def generate_tileset(self):
		self.tileset_list = []
		for y in range(0,self.tileset.get_height(),self.tile_height):
			for x in range(0,self.tileset.get_width(),self.tile_width):
				self.tileset_list.append(pygame.transform.scale(self.tileset.subsurface((x,y),(self.tile_width,self.tile_height)),(tile_size,tile_size)))
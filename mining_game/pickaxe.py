import pygame

class Pickaxe:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load("./mining_game/bloc_pics/iron_pickaxe.png")


    def update(self, mouse_x, mouse_y):
        self.x = mouse_x
        self.y = mouse_y

    def draw(self, screen):
        offset = 4
        screen.blit(self.image, (self.x - self.width / offset, self.y - self.height / offset))

    def scale(self, factor):
        old_width, old_height = self.image.get_size()
        new_width = int(old_width * factor)
        new_height = int(old_height * factor)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.width = new_width
        self.height = new_height
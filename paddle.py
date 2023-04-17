class Paddle(pygame.sprite.Sprite):  # inherits from pygame sprite.Sprite
    def __init__(self):
        # width is 70 height is 80. do these need to be local variables?
        __width__ = 70
        __height__ = 80

        super().__init__()

        self.image = pygame.image.load('astro_shield.png')

        # Move paddle methods
    def moveLeft(self):
        self.rect.x -= 8
        # prevents the paddle from moving off the screen
        if self.rect.x < 0:
            self.rect.x = 0

    def moveRight(self):
        self.rect.x += 8
        # prevents the paddle from moving off the screen
        if self.rect.x > 700:
            self.rect.x = 700
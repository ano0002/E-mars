import pygame

pygame.init()

#Create a screen of 1920x1080 in fullscreen mode
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

playing = True

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
    
    pygame.display.flip()
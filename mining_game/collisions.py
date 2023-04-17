import pygame
from random import random, randint


bt = 20         # size between two tiles up and down
part_num = 15   # number of particles created when a block is broken

def detect_collision(mousepos, level, particle_engine):
    for i, sprite in enumerate(level.terrain_sprites):
        rect = sprite.rect
        
        if rect.collidepoint(mousepos):
            #print(i,sprite)
            if sprite.index == -1:
                break   # if tile is already blank
            
            elif sprite.index == 0:
                pygame.mixer.Sound("./sounds/bedrock.mp3").play()
                break   # if tile is bedrock

            elif sprite.index == 28:
                pygame.mixer.Sound("./sounds/dirt.mp3").play()
                sprite.index = -1
                sprite.image = pygame.Surface((0, 0))
                particle_engine.create_particles(mousepos[0], mousepos[1], part_num, (143,92,51)) 
                particle_engine.create_particles(mousepos[0], mousepos[1], 5, (53,143,68)) 
                break   # if tile is  dirt (only on the right edge)

            elif (level.terrain_sprites.sprites()[i+1].index == -1 or level.terrain_sprites.sprites()[i-1].index == -1 or level.terrain_sprites.sprites()[i+bt].index == -1  or level.terrain_sprites.sprites()[i-bt].index == -1):
                if sprite.index in (25, 26, 27):
                    pygame.mixer.Sound("./sounds/dirt.mp3").play()
                    particle_engine.create_particles(mousepos[0], mousepos[1], part_num, (143,92,51))
                    if sprite.index in (25, 26): particle_engine.create_particles(mousepos[0], mousepos[1], 5, (126,119,128))
                else:
                    pygame.mixer.Sound("./sounds/stone.mp3").play()
                    if sprite.index in (12, 14, 20, 21, 22, 23, 24): particle_engine.create_particles(mousepos[0], mousepos[1], part_num, (135,133,145))
                    elif sprite.index in (1, 2, 3, 4, 5, 6, 7, 8): particle_engine.create_particles(mousepos[0], mousepos[1], part_num, (61,64,78))
                    if sprite.index in (7, 12, 14): particle_engine.create_particles(mousepos[0], mousepos[1], 5, (221,164,126))
                    elif sprite.index == 8: particle_engine.create_particles(mousepos[0], mousepos[1], 5, (17,12,20))
                    elif sprite.index == 6: particle_engine.create_particles(mousepos[0], mousepos[1], 5, (227,85,60))
                    elif sprite.index == 5: particle_engine.create_particles(mousepos[0], mousepos[1], 5, (212,151,30))
                sprite.index = -1
                sprite.image = pygame.Surface((0, 0))
                break   # if tile has a blank tile next to it


def display_ore(name, blocks_left, index, screen, screen_size):
    x = screen_size[0]//20 + screen_size[0]//6 * index      # Coordinates of the ore image
    y = screen_size[1]-screen_size[1]//20
    image = pygame.image.load("./bloc_pics/"+name+".png")   # Ore image
    factor = 3
    old_width, old_height = image.get_size()
    new_width = int(old_width * factor)
    new_height = int(old_height * factor)
    image = pygame.transform.scale(image, (new_width, new_height))
    image_rect = image.get_rect()
    image_rect.center = (x,y)
    screen.blit(image, image_rect)
    font = pygame.font.Font(None, 36)                       # Ore amount
    text = font.render('x '+str(blocks_left[index]), True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (x+40,y)
    screen.blit(text, text_rect)


def detect_blocks_left(level, screen, screen_size, particle_engine):
    blocks_left = [2, 3, 2, 6, 2]      # (5, 6, 8, (7, 12), 14) indexes of rare blocks
    for sprite in level.terrain_sprites:
        if sprite.index == 5:          # gold
            blocks_left[0] -= 1
        elif sprite.index == 6:        # redstone
            blocks_left[1] -= 1
        elif sprite.index == 8:        # coal
            blocks_left[2] -= 1
        elif sprite.index in (7,12):   # iron 
            blocks_left[3] -= 1
        elif sprite.index == 14:       # copper
            blocks_left[4] -= 1

    if blocks_left == [2, 3, 2, 6, 2]:                                # If no blocks are left
        font = pygame.font.Font(None, 36)                             # Text "New gun Crafted!"
        text = font.render("New gun Crafted!", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (screen_size[0] // 2, screen_size[1] // 2)
        screen.blit(text, text_rect)
        image = pygame.image.load('./bloc_pics/gun.png')              # Image of new gun
        factor = 4.5
        old_width, old_height = image.get_size()
        new_width = int(old_width * factor)
        new_height = int(old_height * factor)
        image = pygame.transform.scale(image, (new_width, new_height))
        image_rect = image.get_rect()
        image_rect.center = (screen_size[0] // 2, screen_size[1] // 2 + 50)
        screen.blit(image, image_rect)
        color = (randint(0, 255), randint(0, 255), randint(0, 255))   # Particles
        particle_engine.create_particles(image_rect.center[0], image_rect.center[1], 1, color, 2)
        font = pygame.font.Font(None, 36)                             # Text "Press space to continue"
        text = font.render("Press space to continue", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (screen_size[0] // 2, screen_size[1] - screen_size[1] // 20)
        screen.blit(text, text_rect)
        return False
    else :                                                            # If blocks are left diplay their amount
        display_ore("gold", blocks_left, 0, screen, screen_size)
        display_ore("redstone", blocks_left, 1, screen, screen_size)
        display_ore("coal", blocks_left, 2, screen, screen_size)
        display_ore("iron", blocks_left, 3, screen, screen_size)
        display_ore("copper", blocks_left, 4, screen, screen_size)
        return True
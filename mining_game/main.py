import pygame
from level import Level
from pickaxe import Pickaxe
from collisions import detect_collision, detect_blocks_left
from particles import ParticleEngine


pygame.init()
screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen_color = (117,64,36)  #(185,110,84)
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
pygame.display.set_caption("MINING ALL DAY")
clock = pygame.time.Clock()

music = pygame.mixer.music.load('./sounds/BGM.mp3')
pygame.mixer.music.set_volume(0.4)   # set the volume to 40% otherwise we can't hear the sound effects
music = pygame.mixer.music.play(-1)

level = Level("./bloc_pics/map.csv",screen)

pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))   # hide the mouse cursor
pickaxe = Pickaxe(100, 100, 64, 64)
pickaxe.scale(2.0)   # make the pickaxe twice as big

particle_engine = ParticleEngine(50)   # maximum of 50 particles on screen at once

done = False
while True:
    screen.fill(screen_color)
    if done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                detect_collision(mouse_pos, level, particle_engine)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                detect_collision(mouse_pos, level, particle_engine)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    exit()

    level.run()   # Blocks

    particle_engine.update()  
    particle_engine.draw(screen)   # Particles
    
    done = detect_blocks_left(level, screen, screen_size, particle_engine)   # if there are no blocks left

    mouse_x, mouse_y = pygame.mouse.get_pos()
    pickaxe.update(mouse_x, mouse_y)
    pickaxe.draw(screen)   # Pickaxe

    pygame.display.update()
    clock.tick(60)
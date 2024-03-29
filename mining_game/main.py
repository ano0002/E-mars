from typing import List, Tuple

import pygame
from .level import Level
from .pickaxe import Pickaxe
from .collisions import detect_collision, detect_blocks_left, animation
from .particles import ParticleEngine
import time

def mining_game(screen : pygame.Surface, screen_size : Tuple[int,int], time_delta:int) -> tuple:
    
    #start time in seconds
    start_time = time.time()
    screen_color = (117,64,36)  #(185,110,84)
    clock = pygame.time.Clock()

    music = pygame.mixer.music.load('./mining_game/sounds/BGM.mp3')
    pygame.mixer.music.set_volume(0.4)   # set the volume to 40% otherwise we can't hear the sound effects
    music = pygame.mixer.music.play(-1)

    level = Level("./mining_game/bloc_pics/map.csv",screen)

    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))   # hide the mouse cursor
    pickaxe = Pickaxe(100, 100, 64, 64)   # 100 is the x and y position of the pickaxe, 64 is the width and height of the pickaxe
    pickaxe.scale(1.4)   # make the pickaxe twice as big

    particle_engine = ParticleEngine(50)   # maximum of 50 particles on screen at once

    bubble = pygame.image.load("./set_bubbles/5_mininggame.png")
    is_bubble = True

    done = False
    anim = None
    i_anim, i_anim2 = 200, 1
    while True:
        screen.fill(screen_color)
        if is_bubble:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    is_bubble = False
        else :
            if done:
                if anim is None: anim = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        detect_collision(mouse_pos, level, particle_engine)
                    if (
                        event.type == pygame.KEYDOWN
                        and event.key == pygame.K_SPACE
                    ):
                        return time_delta
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse_pos = pygame.mouse.get_pos()
                            bombs = detect_collision(mouse_pos, level, particle_engine)
                            if bombs:
                                time_delta += 30

        level.run()   # Blocks

        particle_engine.update()
        particle_engine.draw(screen)   # Particles
        done = detect_blocks_left(level, screen, screen_size, particle_engine, anim)   # if there are no blocks left

        if anim:
            animation("gold",    screen, screen_size, round(i_anim))
            animation("redstone",screen, screen_size, round(i_anim))
            animation("coal",    screen, screen_size, round(i_anim))
            animation("iron",    screen, screen_size, round(i_anim))
            animation("copper",  screen, screen_size, round(i_anim))
            if i_anim2 > 2: i_anim -= 0.05 + i_anim2
            i_anim2 += 0.05
            if i_anim <= 0: anim = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        pickaxe.update(mouse_x, mouse_y)
        pickaxe.draw(screen)   # Pickaxe

        if is_bubble:
            screen.blit(bubble,(screen_size[0]/2-bubble.get_width()/2,screen_size[1]-bubble.get_height()))
        else :
            time_delta = time_delta + time.time() - start_time
            time_elapsed = round(time_delta,3)
            start_time = time.time()
            time_text = pygame.font.SysFont('Consolas', 30).render(str(time_elapsed), False, (255, 255, 255))
            screen.blit(time_text,(screen_size[0]/2,0))

        start_time = time.time()
        
        pygame.display.update()
        clock.tick(60)
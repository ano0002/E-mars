import pygame
from player import Player
from tilemap import Map,Tileset
from bubbleshooter.bubbleshoot import bubble_shooter
from mining_game.main import mining_game
#from tower_defense.main import Game as TowerDefense
pygame.init()


pygame.display.set_caption('E-Mars')

#set the display to full screen

tileset = Tileset('./tiled_map/terrain.png')
playing_area = Map('./tiled_map/map', tileset,offset=[0,100], size=[80,45])
player = Player(playing_area)

#display_width, display_height = (pygame.display.Info().current_w, pygame.display.Info().current_h)
#c moins beugé avec ça mais ça fait des bandes noires a cause de la taille des tiles
#je sais pas faire mais si y a moyen de changer la taille des tiles en fonction de la taille de l'écran plutot ce serait moins beugé
display_width = playing_area.width*16
display_height = playing_area.height*16
display = pygame.display.set_mode((display_width, display_height),pygame.FULLSCREEN)

# load the icon image
icon = pygame.image.load("./assets/icon.png")
# set the taskbar icon
pygame.display.set_icon(icon)

#set the player to the middle of the screen
player.rect.center = (display_width/2,2*display_height/3)

clock = pygame.time.Clock()

music = pygame.mixer.music.load('./music/Vast Surroundings (LOOP).mp3')

music = pygame.mixer.music.play(-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.velocity[1] = -10
            if event.key == pygame.K_1:
                validated,score_bubble = bubble_shooter(screen_size=(display_width,display_height),screen=display)
            if event.key == pygame.K_2:
                mining_game(screen=display,screen_size=(display_width,display_height))
                #show back the default cursor
                pygame.mouse.set_cursor((8, 8), (0, 0), (1, 1, 1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1, 1, 1))
                #TowerDefense(display=display)
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot(mouse_pos=pygame.mouse.get_pos())
    player.update(display)
    display.fill((0,0,0))
    playing_area.show_map(display)
    player.draw(display)
    pygame.display.update()
    clock.tick(60)
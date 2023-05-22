import pygame
import time
#from moviepy.editor import*
from player import Player
from tilemap import Map, Tileset
from gemmecatcher.gemmecatcher import gemmecatcher
from mining_game.main import mining_game
from wall_breaker.run import wallbreaker

#from tower_defense.main import Game as TowerDefense
pygame.init()


pygame.display.set_caption('E-Mars')

#INTRO
#clip = VidoeFileClip('.\sfx\INTRO-BOOM.mpg')
#clip.preview()

#END
#clip = VidoeFileClip('.\sfx\END-MARS-TO-EARTH.mpg')
#clip.preview()

#CREDITS
#clip = VidoeFileClip('.\sfx\CREDITS.mpg')
#clip.preview()



#set the display to full screen

tileset = Tileset('./tiled_map/terrain.png')
playing_area = Map('./tiled_map/map', tileset,offset=[0,900], size=[80,45])
player = Player(playing_area)

#display_width, display_height = (pygame.display.Info().current_w, pygame.display.Info().current_h)
#c moins beugé avec ça mais ça fait des bandes noires a cause de la taille des tiles
#je sais pas faire mais si y a moyen de changer la taille des tiles en fonction de la taille de l'écran plutot ce serait moins beugé
display_width, display_height = playing_area.width*16, playing_area.height*16
display = pygame.display.set_mode((display_width, display_height),pygame.FULLSCREEN)

# load the icon image
icon = pygame.image.load("./assets/icon.png")
# set the taskbar icon
pygame.display.set_icon(icon)

#set the player to the middle of the screen
player.rect.center = (display_width/2,2*display_height/3)

clock = pygame.time.Clock()

music = pygame.mixer.music.load('./music/Vast Surroundings (LOOP).mp3')

#music = pygame.mixer.music.play(-1)

# menu loop
condition = True
while condition:
    #use the standard map as a background display a message and wait for the user to press space
    display.fill((0,0,0))
    playing_area.show_map(display)
    text = pygame.font.SysFont('Comic Sans MS', 30).render('Press space to start', False, (255, 255, 255))
    #display welcome message on top of the previous message
    text_welcome = pygame.font.SysFont('Comic Sans MS', 30).render('Welcome to E-Mars', False, (255, 255, 255))
    display.blit(text_welcome,(display_width/2-text.get_width()/2,display_height/2-60))
    display.blit(text,(display_width/2-text_welcome.get_width()/2,display_height/2+25))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            condition = False



#start time in seconds
start_time = round(time.time(),3)
time_delta = 0

counter_mining = 0

while True:
    pos_x = player.rect.x
    pos_y = playing_area.offset[1]*16
    if pos_x > 1100 and pos_x < 1200 and pos_y > 14300 and pos_y < 14700 and counter_mining == 0:
        mining_game(screen=display,screen_size=(display_width,display_height),start_time=start_time,time_delta=time_delta)
        pygame.mouse.set_cursor((8, 8), (0, 0), (1, 1, 1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1, 1, 1))
        counter_mining += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.velocity[1] = -10
            if event.key == pygame.K_1:
                time_delta= gemmecatcher(screen_size=(display_width,display_height),screen=display,delta_time=time_delta)
            if event.key == pygame.K_3:
                wallbreaker(screen=display,screen_size=(display_width,display_height),time_delta=time_delta)
                #59, 701-705
                for i in range(701,706):
                    playing_area.map[i][58] = 23
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot(mouse_pos=pygame.mouse.get_pos())
    player.update(display)
    display.fill((0,0,0))
    playing_area.show_map(display)
    player.draw(display)
    time_elapsed = round(time.time() - start_time + time_delta,3)
    #display the time elapsed on the top middle of the screen
    #use Consolas font
    time_text = pygame.font.SysFont('Consolas', 30).render(str(time_elapsed), False, (255, 255, 255))
    display.blit(time_text,(display_width/2,0))
    pygame.display.update()
    clock.tick(60)
    pos_x = player.rect.x
    pos_y = playing_area.offset[1]*16
    print(pos_x,pos_y)

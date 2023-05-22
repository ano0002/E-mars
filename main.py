import pygame
import time
try :
    import cv2
    opencv = True
except :
    print("OpenCV not installed")
    print("Please install OpenCV with the command : pip install opencv-python")
    print("If you want the full experience")
    opencv = False
from player import Player
from tilemap import Map, Tileset
from gemmecatcher.gemmecatcher import gemmecatcher
from mining_game.main import mining_game
from wall_breaker.run import wallbreaker

pygame.init()

pygame.font.init()

pygame.display.set_caption('E-Mars')


#END
#clip = VidoeFileClip('.\sfx\END-MARS-TO-EARTH.mpg')
#clip.preview()

#CREDITS
#clip = VidoeFileClip('.\sfx\CREDITS.mpg')
#clip.preview()



# load the icon image
icon = pygame.image.load("./assets/icon.png")
# set the taskbar icon
pygame.display.set_icon(icon)


#set the display to full screen

tileset = Tileset('./tiled_map/terrain.png')
playing_area = Map('./tiled_map/map', tileset,offset=[0,900], size=[80,45])
player = Player(playing_area)

display_width, display_height = playing_area.width*16, playing_area.height*16
display = pygame.display.set_mode((display_width, display_height),pygame.FULLSCREEN)


clock = pygame.time.Clock()


if opencv :
    
    #INTRO
    video = cv2.VideoCapture(".\\sfx\\INTRO-BOOM.mpg")
    fps = video.get(cv2.CAP_PROP_FPS)


    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                exit()
        playing, video_image = video.read()
        if playing:
            video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            video_surf = pygame.transform.scale(video_surf, (display_width, display_height))

        display.blit(video_surf, (0, 0))
        pygame.display.update()
        clock.tick(fps)


#set the player to the middle of the screen
player.rect.center = (display_width/2,2*display_height/3)


pygame.mixer.music.set_volume(0.1)

music = pygame.mixer.music.load('./music/Vast Surroundings (LOOP).mp3')

music = pygame.mixer.music.play(-1)

consolas = pygame.font.SysFont('Consolas', 30)

consolas_bold = pygame.font.SysFont('Consolas', 31)
consolas_bold.bold = True

# menu loop  
padding = 15
text = consolas.render('Press space to start', True, (255, 255, 255))
text_rect=text.get_rect(center=(display_width/2, display_height/2+25))

button_rect = text.get_rect(center=(display_width/2, display_height/2+25))
button_rect.x -= padding
button_rect.y -= padding
button_rect.width += padding*2
button_rect.height += padding*2
button_pressed = False

text_welcome = consolas.render('Welcome to E-Mars', True, (255, 255, 255))

text_welcome2 = consolas_bold.render('Welcome to E-Mars', True, (000, 000, 000))


while not button_pressed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                button_pressed = True
        elif event.type == pygame.MOUSEBUTTONDOWN :
            if button_rect.collidepoint(event.pos) :
                button_pressed=True



    display.fill((0,0,0))
    playing_area.show_map(display)

    # Draw button
    button_color = (255, 255, 255) if button_rect.collidepoint(pygame.mouse.get_pos()) else (190, 190, 190)
    pygame.draw.rect(display, button_color, button_rect, 4)

    # Display text  
    display.blit(text_welcome2,(display_width/2-text_welcome2.get_width()/2,display_height/2-62))
    display.blit(text_welcome,(display_width/2-text_welcome.get_width()/2,display_height/2-60))
    display.blit(text, text_rect)

    pygame.display.update()
    clock.tick(60)
    









#start time in seconds
start_time = round(time.time(),3)
time_delta = 0

counter_mining = 0
counter_wallbreaker = 0

playing = True

while playing:
    pos_x = player.rect.x
    pos_y = playing_area.offset[1]*16
    if pos_x > 1100 and pos_x < 1200 and pos_y > 14300 and pos_y < 14700 and counter_mining == 0:
        time_delta = mining_game(screen=display,screen_size=(display_width,display_height),time_delta=time_delta)
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        counter_mining += 1
        music = pygame.mixer.music.load('./music/Vast Surroundings (LOOP).mp3')
        music = pygame.mixer.music.play(-1)
        start_time = time.time()
    #911 10798
    if pos_x > 890 and pos_x < 1050 and pos_y > 10770 and pos_y < 10800 and counter_wallbreaker == 0:
        time_delta = wallbreaker(screen=display,screen_size=(display_width,display_height),time_delta=time_delta)
        counter_wallbreaker += 1
        for i in range(701,706):
            playing_area.map[i][59] = 23
    
    if pos_x > 800 and pos_y <7850 :
        playing = False
        break
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player.shoot(mouse_pos=pygame.mouse.get_pos())
    player.update(display)
    display.fill((0,0,0))
    playing_area.show_map(display)
    player.draw(display)
    time_delta += time.time() - start_time
    start_time = time.time()
    time_elapsed = round(time_delta,3)
    #display the time elapsed on the top middle of the screen
    #use Consolas font
    time_text = consolas.render(str(time_elapsed), False, (255, 255, 255))
    display.blit(time_text,(display_width/2,0))
    
    pos_x = player.rect.x
    pos_y = playing_area.offset[1]*16
    pos_pers = consolas.render(str([pos_x,pos_y]), False, (255, 255, 255))
    display.blit(pos_pers,(0,0))
    pygame.display.update()
    clock.tick(60)
    
time_delta= gemmecatcher(screen_size=(display_width,display_height),screen=display,delta_time=time_delta)

if opencv :
    #OUTRO
    video = cv2.VideoCapture(".\\sfx\\END-MARS-TO-EARTH.mpg")
    fps = video.get(cv2.CAP_PROP_FPS)


    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                exit()
        playing, video_image = video.read()
        if playing:
            video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            video_surf = pygame.transform.scale(video_surf, (display_width, display_height))

        display.blit(video_surf, (0, 0))
        pygame.display.update()
        clock.tick(fps)
        
print("You have finished the game in",time_delta,"seconds")
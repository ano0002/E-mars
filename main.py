import pygame
from player import Player
from tilemap import Map,Tileset

pygame.init()


pygame.display.set_caption('E-Mars')

#set the display to full screen


display = pygame.display.set_mode((40*16, 60*16),pygame.FULLSCREEN)
clock = pygame.time.Clock()

tileset = Tileset('./tiled_map/terrain.png')
playing_area = Map('./tiled_map/map.csv', tileset,offset=[0,60])
player = Player(playing_area,position=[20*16,45*16])


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.velocity[1] = -10
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot(mouse_pos=pygame.mouse.get_pos(),power=10)
    player.update(display)
    display.fill((0,0,0))
    playing_area.show_map(display)
    player.draw(display)
    pygame.display.update()
    clock.tick(60)
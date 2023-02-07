import pygame
if __name__ == "__main__":
    from terrain import Terrain
    pygame.init()
    pygame.display.set_caption("Terrain")
    display = pygame.display.set_mode((800, 600))
    terrain = Terrain("./tiled_map/map.csv")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.fill((0,0,0))
        terrain.draw(display)
        pygame.display.update()
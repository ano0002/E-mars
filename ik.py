import pygame,math
from pygame.math import Vector2

pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)

points = list(map(Vector2, [(100, 100), (125, 100), (150, 100)]))
target = Vector2(450, 300)

rel_points = []
angles = []

for i in range(1, len(points)):
    rel_points.append(points[i] - points[i-1])
    angles.append(0)

def solve_ik(i, endpoint, target):
    if i < len(points) - 2:
        endpoint = solve_ik(i+1, endpoint, target)
    current_point = points[i]

    angle = (endpoint-current_point).angle_to(target-current_point)
    angles[i] += angle

    return current_point + (endpoint-current_point).rotate(angle)

clock = pygame.time.Clock()
gun = pygame.transform.scale(pygame.image.load('./assets/gun.png'), (25, 25))

while 1:
    target = Vector2(pygame.mouse.get_pos())
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            exit()

    solve_ik(0, points[-1], target)

    angle = 0
    for i in range(1, len(points)):
        angle += angles[i-1]
        points[i] = points[i-1] + rel_points[i-1].rotate(angle)
    
    screen.fill((255,255,255))
    
    for i,angle in enumerate(angles):
        rotimage = pygame.transform.rotate(gun,-angle-sum(angles[:i]))
        rect = rotimage.get_rect(center=(Vector2(points[i])+Vector2(points[i+1]))/2)
        screen.blit(rotimage, rect)
    
    pygame.display.update()
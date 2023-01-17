#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #

import pygame
from pygame.math import Vector2

def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

class Particle:
    def __init__(self, pos, vel, timer,color,radius,gravity,glow_radius=0):
        self.pos = pos
        self.vel = vel.copy()
        self.timer = timer
        self.color = color
        self.radius = radius
        self.gravity = gravity
        self.alive = True
        self.glow_radius = glow_radius
    
    def update(self):
        self.pos += self.vel
        self.vel[1] += self.gravity
        self.vel[0] *= 0.9
        
        self.timer -= 1
        if self.timer <= 0:
            self.alive = False
    
    def draw(self,screen):
        if self.glow_radius > 0:
            surf = circle_surf(self.glow_radius, list(x*0.2 for x in self.color))
            screen.blit(surf, (self.pos[0]-self.glow_radius, self.pos[1]-self.glow_radius), special_flags=pygame.BLEND_RGB_ADD)
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

class Particle_Emitter:
    def __init__(self, rate, pos, vel, color = (255,255,255), radius = 5, gravity = 0.1,timer=50,glow_radius=0):
        self.rate = rate
        self.pos = pos
        self.vel = vel
        self.color = color
        self.radius = radius
        self.gravity = gravity
        self.particles = []
        self.frame = 0
        self.timer = timer
        self.glow_radius = glow_radius
        
    def update(self):
        self.frame += 1
        self.vel[0] = random.random()*4-2
        if self.frame % self.rate == 0:
            self.particles.append(Particle(self.pos, self.vel, self.timer, self.color, self.radius, self.gravity, self.glow_radius))
        
        for particle in self.particles:
            particle.update()
            if not particle.alive:
                self.particles.remove(particle)
                del particle
    
    def draw(self,screen):
        for particle in self.particles:
            particle.draw(screen)

if __name__ == '__main__':
    import pygame,random

    mainClock = pygame.time.Clock()
    from pygame.locals import *
    pygame.init()
    pygame.display.set_caption('game base')
    screen = pygame.display.set_mode((500, 500),0,32)

    emitter = Particle_Emitter(rate = 10, pos = Vector2(250, 250), vel = Vector2(1, -5),timer = 50,glow_radius=15,color=(255,0,0))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        emitter.update()
        emitter.pos = pygame.mouse.get_pos()
        screen.fill((0,0,0))
        emitter.draw(screen)
        pygame.display.update()
        mainClock.tick(60)
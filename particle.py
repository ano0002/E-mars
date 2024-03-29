#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #

import pygame,random
from pygame.math import Vector2
from typing import Tuple, List


def circle_surf(radius, color, alpha):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_alpha(alpha)
    return surf

class Particle:
    def __init__(self, pos, vel, timer,color,radius,gravity,glow_color,glow_radius=0):
        self.pos = pos
        self.vel = vel.copy()
        self.timer = timer
        self.max_timer = timer
        self.color = color
        self.radius = radius
        self.gravity = gravity
        self.alive = True
        self.glow_radius = glow_radius
        self.alpha = 255
        self.glow_color = glow_color

    def update(self):
        self.pos += self.vel
        self.vel[1] += self.gravity
        self.vel[0] *= 0.9
        self.alpha = int(255 * self.timer / self.max_timer)
        self.timer -= 1
        if self.timer <= 0:
            self.alive = False

    def draw(self,screen):
        if self.glow_radius > 0:
            surf = circle_surf(self.glow_radius, self.glow_color,self.alpha)
            screen.blit(surf, (self.pos[0]-self.glow_radius, self.pos[1]-self.glow_radius), special_flags=pygame.BLEND_ADD)
        pygame.draw.circle(screen, (*self.color,self.alpha), self.pos, self.radius)

class Particle_Emitter:
    def __init__(self, rate, pos, vel, color = (255,255,255), glow_color = (200,200,200), radius = 5, gravity = 0.1,timer=50,glow_radius=0):
        self.rate = rate
        self.pos = pos
        self.vel = list(vel)
        self.color = color
        self.radius = radius
        self.gravity = gravity
        self.particles = []
        self.frame = 0
        self.timer = timer
        self.glow_radius = glow_radius
        self.glow_color = glow_color

    def update(self):
        self.frame += 1
        vel = self.vel.copy()
        if hasattr(self.vel[0],"__call__"):
            vel[0] = self.vel[0]()
        if hasattr(self.vel[1],"__call__"):
            vel[1] = self.vel[1]()
        if self.frame % self.rate == 0:
            self.particles.append(Particle(self.pos, Vector2(vel), self.timer, self.color, self.radius, self.gravity,self.glow_color, self.glow_radius))

        for particle in self.particles:
            particle.update()
            if not particle.alive:
                self.particles.remove(particle)
                del particle

    def draw(self,screen):
        for particle in self.particles:
            particle.draw(screen)

class Torch(Particle_Emitter):
    def __init__(self, tile_pos,offset):
        super().__init__(
            rate=1,
            pos=[i * 16 for i in tile_pos],
            vel=(
                lambda: random.random() * 4 - 2,
                lambda: -random.random() * 4 - 2,
            ),
            timer=20,
            radius=1,
            glow_radius=5,
            color=(255, 0, 0),
            glow_color=(50, 0, 0),
        )
        self.offset = offset
        self.tile_pos = tile_pos
    def update(self,offset):
        self.offset = offset
        self.pos = [
            i * 16
            for i in (
                self.tile_pos[0] - self.offset[0],
                self.tile_pos[1] - self.offset[1],
            )
        ]
        super().update()

if __name__ == '__main__':
    import pygame,random

    mainClock = pygame.time.Clock()
    from pygame.locals import *
    pygame.init()
    pygame.display.set_caption('game base')
    screen = pygame.display.set_mode((500, 500),0,32)

    emitter = Particle_Emitter(rate =1, pos = Vector2(250, 250),
                               vel = (lambda : random.random()*4-2, lambda : -random.random()*4-2),
                               timer = 20,radius = 1,
                               glow_radius=5,color=(255,0,0),glow_color=(50,0,0))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        emitter.update()
        emitter.pos = pygame.mouse.get_pos()
        screen.fill((33,31,48))
        emitter.draw(screen)
        pygame.display.update()
        mainClock.tick(60)
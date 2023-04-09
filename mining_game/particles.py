import pygame
from random import randint, uniform
from math import pi, cos, sin


class Particle:
    def __init__(self, x, y, size, speed, color, gravity=3):
        self.x = x
        self.y = y
        self.size = size
        self.color = color   # color should be the same as the block that was broken
        self.speed = speed
        self.angle = uniform(0, 2 * pi)
        self.gravity = gravity
        
    def update(self):
        self.x += cos(self.angle) * self.speed
        self.y += sin(self.angle) * self.speed + self.gravity
        self.size -= 0.5
        if self.size < 0:
            self.size = 0
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - self.size / 2, self.y - self.size / 2, self.size, self.size))
        

class ParticleEngine:
    def __init__(self, max_particles):
        self.max_particles = max_particles
        self.particles = []
        
    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.size == 0:
                self.particles.remove(particle)
                
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
            
    def create_particles(self, x, y, num_particles, color, gravity=3):
        for i in range(num_particles):
            size = randint(5, 20)
            speed = uniform(1, 5)
            particle = Particle(x, y, size, speed, color, gravity)
            self.particles.append(particle)
            if len(self.particles) > self.max_particles:
                self.particles.pop(0)


if "__main__" == __name__ :
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    particle_engine = ParticleEngine(50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((15, 15, 15))

        particle_engine.update()
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        x, y = pygame.mouse.get_pos()
        particle_engine.create_particles(x, y, 1, color, 2)   # last argument is gravity (particles will go down more, default is 3)
        particle_engine.draw(screen)

        pygame.display.update()
        clock.tick(60)
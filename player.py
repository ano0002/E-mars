import pygame,math
from particle import Particle_Emitter
from pygame.math import Vector2
import random

class Player():
    def __init__(self,tilemap,position = (400,200)) -> None:
        self.image = pygame.transform.scale(pygame.image.load('./assets/player.png'), (32, 64))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.velocity = [0, 0]
        self.gravity = 0.5
        self.gun = pygame.transform.scale(pygame.image.load('./assets/gun.png'), (25, 25))
        self.max_bullets = 3
        self.bullet_count = self.max_bullets
        self.bullets = []
        self.tilemap = tilemap
        self.rects = {
            "top":pygame.Rect(self.rect.x,self.rect.y,self.rect.width,1),
            "bottom":pygame.Rect(self.rect.centerx-1,self.rect.bottom,2,1), 
            "bottom-left":pygame.Rect(self.rect.x,self.rect.bottom,1,1),
            "bottom-right":pygame.Rect(self.rect.right,self.rect.bottom,1,1),
            "left":pygame.Rect(self.rect.x,self.rect.y,1,self.rect.height),
            "right":pygame.Rect(self.rect.right,self.rect.y,1,self.rect.height)
        }
        
    def update(self,display):
        
        self.rect.move_ip(self.velocity)
        self.velocity[0] = round(self.velocity[0] * 0.9,3)
        
        if self.rect.bottom <= 0:
            self.rect.y += 60*16
            self.tilemap.offset[1] -= 60
        if self.rect.top >= 30*32:
            self.rect.move_ip((0,-(60*16)))
            self.tilemap.offset[1] += 60
        
        self.velocity[1] += self.gravity
        
        self.rects = {
            "top":pygame.Rect(self.rect.x,self.rect.y,self.rect.width,1),
            "bottom":pygame.Rect(self.rect.centerx-1,self.rect.bottom,2,1),
            "bottom-left":pygame.Rect(self.rect.x,self.rect.bottom,1,1),
            "bottom-right":pygame.Rect(self.rect.right,self.rect.bottom,1,1),
            "left":pygame.Rect(self.rect.x,self.rect.y,1,self.rect.height),
            "right":pygame.Rect(self.rect.right,self.rect.y,1,self.rect.height)
        }
        
        interactibles = self.tilemap.get_interactibles(display)
        if self.rect.collidelist(interactibles) != -1:
            self.tilemap.interact(interactibles[self.rect.collidelist(interactibles)],self,display)
            
        colliders = self.tilemap.get_colliders(display)
        
        if self.rects["bottom"].collidelist(colliders) != -1 and (self.rects["bottom-left"].collidelist(colliders) != -1 or self.rects["bottom-right"].collidelist(colliders) != -1):
            self.velocity[1] = 0
            self.bullet_count = self.max_bullets
            while self.rects["bottom"].collidelist(colliders) != -1:
                self.rect.move_ip(0,-1)
                self.rects = {
                    "top":pygame.Rect(self.rect.x,self.rect.y,self.rect.width,1),
                    "bottom":pygame.Rect(self.rect.centerx-1,self.rect.bottom,2,1),
                    "bottom-left":pygame.Rect(self.rect.x,self.rect.bottom,1,1),
                    "bottom-right":pygame.Rect(self.rect.right,self.rect.bottom,1,1),
                    "left":pygame.Rect(self.rect.x,self.rect.y,1,self.rect.height),
                    "right":pygame.Rect(self.rect.right,self.rect.y,1,self.rect.height)
                }
        
        elif self.rects["top"].collidelist(colliders) != -1:
            self.velocity[1] = self.gravity*2
        
        if self.rects["left"].collidelist(colliders) != -1 or self.rect.x <=0 :
            self.velocity[0] = abs(self.velocity[0])
            if self.rect.x <=0 :
                self.rect.x = 0
                self.rects = {
                    "top":pygame.Rect(self.rect.x,self.rect.y,self.rect.width,1),
                    "bottom":pygame.Rect(self.rect.centerx-1,self.rect.bottom,2,1),
                    "bottom-left":pygame.Rect(self.rect.x,self.rect.bottom,1,1),
                    "bottom-right":pygame.Rect(self.rect.right,self.rect.bottom,1,1),
                    "left":pygame.Rect(self.rect.x,self.rect.y,1,self.rect.height),
                    "right":pygame.Rect(self.rect.right,self.rect.y,1,self.rect.height)
                }
        if self.rects["right"].collidelist(colliders) != -1 or self.rect.right>=20*32 :
            self.velocity[0] = -abs(self.velocity[0])
            if self.rect.x >=20*32 :
                self.rect.x = 20*32
                self.rects = {
                    "top":pygame.Rect(self.rect.x,self.rect.y,self.rect.width,1),
                    "bottom":pygame.Rect(self.rect.centerx-1,self.rect.bottom,2,1),
                    "bottom-left":pygame.Rect(self.rect.x,self.rect.bottom,1,1),
                    "bottom-right":pygame.Rect(self.rect.right,self.rect.bottom,1,1),
                    "left":pygame.Rect(self.rect.x,self.rect.y,1,self.rect.height),
                    "right":pygame.Rect(self.rect.right,self.rect.y,1,self.rect.height)
                }
        if self.rects["bottom-left"].collidelist(colliders) != -1 and not self.rects["bottom"].collidelist(colliders) != -1:
            self.velocity[0] = self.velocity[1]
        if self.rects["bottom-right"].collidelist(colliders) != -1 and not self.rects["bottom"].collidelist(colliders) != -1:
            self.velocity[0] = -self.velocity[1]
        
        for bullet in self.bullets:
            bullet.update(display)
            
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pos = pygame.mouse.get_pos()
        angle = 360-math.atan2(pos[1]-self.rect.centery,pos[0]-self.rect.centerx)*180/math.pi
        rotimage = pygame.transform.rotate(self.gun,angle)
        rect = rotimage.get_rect(center=self.rect.center)
        screen.blit(rotimage, rect)
        for bullet in self.bullets:
            bullet.draw(screen)
        
    def shoot(self,mouse_pos,power):
        if self.bullet_count>0:
            self.bullet_count -= 1
        else:
            return
        angle = math.radians(360-math.atan2(mouse_pos[1]-self.rect.centery,mouse_pos[0]-self.rect.centerx)*180/math.pi)
        self.velocity[0] = -math.cos(angle)*power
        self.velocity[1] = math.sin(angle)*power
        self.bullets.append(Bullet(self.tilemap,self,Vector2(math.cos(angle)*power,-math.sin(angle)*power),power))
        
class Bullet():
    def __init__(self,map,player,velocity,power):
        self.map = map
        self.player = player
        self.rect = pygame.Rect(player.rect.centerx,player.rect.centery,power/2,power/2)
        self.velocity = velocity
        self.gravity = 0.5
        self.emitter = Particle_Emitter(1,self.rect.center,
                                        (lambda:velocity[0]*-0.1+random.random()*3-1.5,lambda:velocity[1]*-0.1+random.random()*3-1.5),
                                        color=(60,60,0),
                                        gravity=0,
                                        radius=power/4,
                                        timer=power/4)
    
    def update(self,display):
        self.rect.move_ip(self.velocity)
        self.emitter.pos = self.rect.center
        if self.rect.bottom >= 60*16:
            self.player.bullets.remove(self)
        if self.rect.bottom <= 0:
            self.player.bullets.remove(self)
        colliders = self.map.get_colliders(display)
        interactibles = self.map.get_interactibles(display)
        if self.rect.collidelist(interactibles) != -1:
            self.map.shot(interactibles[self.rect.collidelist(interactibles)],self.player,display)
        if self.rect.collidelist(colliders) != -1:
            self.player.bullets.remove(self)
        self.emitter.update()
        
    def draw(self,screen):
        pygame.draw.circle(screen,(255,255,0),(self.rect.x,self.rect.y),self.rect.width/2)
        self.emitter.draw(screen)

if __name__ == "__main__":
    from tilemap import Map,Tileset
    
    pygame.init()
    display = pygame.display.set_mode((40*16, 60*16))
    clock = pygame.time.Clock()
    
    tileset = Tileset('./tiled_map/terrain.png')
    playing_area = Map('./tiled_map/map.csv', tileset,offset=[0,60])
    player = Player(playing_area)
    
    
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
        for rect in player.rects.values():
            pygame.draw.rect(display,(0,255,0),rect,1)
        for collider in playing_area.get_colliders(display):
            pygame.draw.rect(display,(255,0,0),collider,1)
        for collider in playing_area.get_interactibles(display):
            pygame.draw.rect(display, (0, 0, 255), collider, 1)
        player.draw(display)
        pygame.display.update()
        clock.tick(60)
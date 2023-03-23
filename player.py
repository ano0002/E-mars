import pygame,math
from pygame.math import Vector2

class Player():
    def __init__(self,tilemap,position = (400,200)) -> None:
        self.image = pygame.transform.scale(pygame.image.load('./assets/player.png'), (32, 64))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.velocity = [0, 0]
        self.gravity = 0.5
        self.gun ='./assets/gun.png'
        self.max_bullets = 2
        self.bullet_count = self.max_bullets
        self.bullets = []
        self.tilemap = tilemap
        self.power = 10
        self.rects = {
            "top":pygame.Rect(self.rect.x,self.rect.y,self.rect.width,1),
            "bottom":pygame.Rect(self.rect.centerx-1,self.rect.bottom,2,1), 
            "bottom-left":pygame.Rect(self.rect.x,self.rect.bottom,1,1),
            "bottom-right":pygame.Rect(self.rect.right,self.rect.bottom,1,1),
            "left":pygame.Rect(self.rect.x,self.rect.y,1,self.rect.height),
            "right":pygame.Rect(self.rect.right,self.rect.y,1,self.rect.height)
        }
        self.sounds = {
            "gunshot":pygame.mixer.Sound("./sfx/gunshot.wav"),
            "pickup":pygame.mixer.Sound("./sfx/pickup.wav")
        }

    @property
    def gun(self):
        return self._gun

    @gun.setter
    def gun(self,gun):
        if hasattr(self,"_gun"):
            pygame.mixer.Sound.play(self.sounds["pickup"])
        self._gun =  pygame.transform.scale(pygame.image.load(gun), (25, 25))

    def update(self,display):

        self.rect.move_ip(self.velocity[0],0)

        self.rects = {
            "top":pygame.Rect(self.rect.x,self.rect.y,self.rect.width,1),
            "bottom":pygame.Rect(self.rect.centerx-2,self.rect.bottom,4,1),
            "bottom-left":pygame.Rect(self.rect.x,self.rect.bottom,1,1),
            "bottom-right":pygame.Rect(self.rect.right,self.rect.bottom,1,1),
            "left":pygame.Rect(self.rect.x,self.rect.y,1,self.rect.height),
            "right":pygame.Rect(self.rect.right,self.rect.y,1,self.rect.height)
        }
        last_pos = self.tilemap.offset.copy()[1]

        for _ in range(int(abs(self.velocity[1])//8)):
            colliders = self.tilemap.get_colliders(display)
            if  self.rects["bottom"].collidelist(colliders)!=-1:
                self.tilemap.offset -= Vector2(0,0.5)
                break
            if self.velocity[1] > 0:
                self.tilemap.offset += Vector2(0,0.5)
            else:
                self.tilemap.offset -= Vector2(0,0.5)

        if self.velocity[1] > 0:
            self.tilemap.offset += Vector2(0,self.velocity[1]%8/16)
        else:
            self.tilemap.offset -= Vector2(0,abs(self.velocity[1])%8/16)

        self.velocity[0] = round(self.velocity[0] * 0.9,3)


        self.velocity[1] += self.gravity


        interactibles = self.tilemap.get_interactibles(display)
        collidewith = self.rect.collidelist(interactibles["rects"])
        if collidewith != -1:
            self.tilemap.interact(interactibles["rects"][collidewith],interactibles["tiles"][collidewith],self,display)

        colliders = self.tilemap.get_colliders(display)

        if self.rects["bottom"].collidelist(colliders) != -1 and (self.rects["bottom-left"].collidelist(colliders) != -1 or self.rects["bottom-right"].collidelist(colliders) != -1):
            self.velocity[1] = 0
            if round(self.velocity[0]) == 0:
                self.bullet_count = self.max_bullets
            while self.rects["bottom"].collidelist(colliders) != -1:
                self.tilemap.offset -= (0,1/16)
                colliders = self.tilemap.get_colliders(display)

        elif self.rects["top"].collidelist(colliders) != -1:
            self.velocity[1] = self.gravity*2

        if self.rects["left"].collidelist(colliders) != -1 or self.rect.x <=0 :
            self.velocity[0] = abs(self.velocity[0])
            if self.rect.x <=0 :
                self.rect.x = 0
                self.rects = {
                    "top":pygame.Rect(self.rect.x,self.rect.y,self.rect.width,1),
                    "bottom":pygame.Rect(self.rect.centerx-2,self.rect.bottom,4,1),
                    "bottom-left":pygame.Rect(self.rect.x,self.rect.bottom,1,1),
                    "bottom-right":pygame.Rect(self.rect.right,self.rect.bottom,1,1),
                    "left":pygame.Rect(self.rect.x,self.rect.y,1,self.rect.height),
                    "right":pygame.Rect(self.rect.right,self.rect.y,1,self.rect.height)
                }

        if self.rects["right"].collidelist(colliders) != -1 or self.rect.right>=self.tilemap.width*16  :
            self.velocity[0] = -abs(self.velocity[0])
            if self.rect.right >=self.tilemap.width*16 :
                self.rect.right = self.tilemap.width*16 
                self.rects = {
                    "top":pygame.Rect(self.rect.x,self.rect.y,self.rect.width,1),
                    "bottom":pygame.Rect(self.rect.centerx-2,self.rect.bottom,4,1),
                    "bottom-left":pygame.Rect(self.rect.x,self.rect.bottom,1,1),
                    "bottom-right":pygame.Rect(self.rect.right,self.rect.bottom,1,1),
                    "left":pygame.Rect(self.rect.x,self.rect.y,1,self.rect.height),
                    "right":pygame.Rect(self.rect.right,self.rect.y,1,self.rect.height)
                }

        if self.rects["bottom-left"].collidelist(colliders) != -1 and not self.rects["bottom"].collidelist(colliders) != -1:
            self.velocity[0] = self.velocity[1]
        if self.rects["bottom-right"].collidelist(colliders) != -1 and not self.rects["bottom"].collidelist(colliders) != -1:
            self.velocity[0] = -self.velocity[1]

        new_pos = self.tilemap.offset.copy()[1]

        upper_movement = (new_pos-last_pos)*16


        for bullet in self.bullets:
            bullet.update(display,upper_movement)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pos = pygame.mouse.get_pos()
        angle = 360-math.atan2(pos[1]-self.rect.centery,pos[0]-self.rect.centerx)*180/math.pi
        rotimage = pygame.transform.rotate(self.gun,angle)
        rect = rotimage.get_rect(center=self.rect.center)
        screen.blit(rotimage, rect)
        for bullet in self.bullets:
            bullet.draw(screen)

    def shoot(self,mouse_pos):
        power = self.power
        if self.bullet_count>0:
            self.bullet_count -= 1
        else:
            return
        pygame.mixer.Sound.play(self.sounds["gunshot"])
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

    def update(self,display,upper_movement):
        self.rect.move_ip(self.velocity[0],self.velocity[1]-upper_movement)
        colliders = self.map.get_colliders(display)
        interactibles = self.map.get_interactibles(display)
        interactiblecollision = self.rect.collidelist(interactibles["rects"])
        if interactiblecollision != -1:
            self.map.shot(interactibles["rects"][interactiblecollision],interactibles["tiles"][interactiblecollision],self.player,display)

        if self.rect.bottom >= self.map.height*16:
            self.player.bullets.remove(self)
        elif self.rect.bottom <= 0:
            self.player.bullets.remove(self)
        elif self.rect.right >= self.map.width*16:
            self.player.bullets.remove(self)
        elif self.rect.x <= 0:
            self.player.bullets.remove(self)
        elif self.rect.collidelist(colliders) != -1:
            self.player.bullets.remove(self)

    def draw(self,screen):
        pygame.draw.circle(screen,(255,255,0),(self.rect.x,self.rect.y),self.rect.width/2)

if __name__ == "__main__":
    from tilemap import Map,Tileset

    pygame.init()

    tileset = Tileset('./tiled_map/terrain.png')
    playing_area = Map('./tiled_map/map', tileset,offset=[0,0], size=[80,45])
    player = Player(playing_area)

    display_width = playing_area.width*16
    display_height = playing_area.height*16
    display = pygame.display.set_mode((display_width, display_height))
    player.rect.center = (display_width/2,2*display_height/3)
    clock = pygame.time.Clock()



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.velocity[1] = -16
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot(mouse_pos=pygame.mouse.get_pos())
        player.update(display)
        display.fill((0,0,0))
        playing_area.show_map(display)
        for rect in player.rects.values():
            pygame.draw.rect(display,(0,255,0),rect,1)
        for collider in playing_area.get_colliders(display):
            pygame.draw.rect(display,(255,0,0),collider,1)
        for collider in playing_area.get_interactibles(display)["rects"]:
            pygame.draw.rect(display, (0, 0, 255), collider, 1)
        player.draw(display)
        pygame.display.update()
        clock.tick(60)
import pygame
import math
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):# Load and scale the player image
    def __init__(self, position, tilemap):
        self.list_images = [pygame.transform.scale(pygame.image.load('./assets/player1.png'),(32, 64)), 
                            pygame.transform.scale(pygame.image.load('./assets/player2.png'), (32, 64)),
                            pygame.transform.scale(pygame.image.load('./assets/player3.png'), (32, 64)),
                            pygame.transform.scale(pygame.image.load('./assets/player4.png'), (32, 64)),]
        self.image_index = 0
        self.image = self.list_images[self.image_index]
        self.facing_right, self.facing_left = True, False
        # Set the player's rectangle
        self.rect = self.image.get_rect(center=position)
        # Set the player's velocity and gravity
        self.velocity = [0, 0]
        self.gravity = 0.5
        # Set the player's gun image, bullet count, and max bullets
        self.gun ='./assets/gun.png'
        self.max_bullets = 2
        self.bullet_count = self.max_bullets
        self.bullets = pygame.sprite.Group()
        # Set the tilemap, power, and rectangle dictionaries for the player
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
        # Set the sounds dictionary for the player
        self.sounds = {
            "gunshot":pygame.mixer.Sound("./sfx/gunshot.wav"),
            "pickup":pygame.mixer.Sound("./sfx/pickup.wav")
        }
        self.x = position[0]
        self.y = position[1]

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = value
        self.rects = {
            "top":pygame.Rect(self.rect.x,self.rect.y,self.rect.width,1),
            "bottom":pygame.Rect(self.rect.centerx-1,self.rect.bottom,2,1), 
            "bottom-left":pygame.Rect(self.rect.x,self.rect.bottom,1,1),
            "bottom-right":pygame.Rect(self.rect.right,self.rect.bottom,1,1),
            "left":pygame.Rect(self.rect.x,self.rect.y,1,self.rect.height),
            "right":pygame.Rect(self.rect.right,self.rect.y,1,self.rect.height)
        }
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = value
        self.rects = {
            "top":pygame.Rect(self.rect.x,self.rect.y,self.rect.width,1),
            "bottom":pygame.Rect(self.rect.centerx-1,self.rect.bottom,2,1), 
            "bottom-left":pygame.Rect(self.rect.x,self.rect.bottom,1,1),
            "bottom-right":pygame.Rect(self.rect.right,self.rect.bottom,1,1),
            "left":pygame.Rect(self.rect.x,self.rect.y,1,self.rect.height),
            "right":pygame.Rect(self.rect.right,self.rect.y,1,self.rect.height)
        }

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.bullets.draw(surface)
        
    def update(self):
        self.velocity[1] -= self.gravity
        
        if self.velocity[1] > 0:
            if raycast(self.rects["top"].center,self.tilemap.get_colliders(),(0,1),abs(self.velocity[1])):
                self.velocity[1] = 0
                print("top")
        else :
            if raycast(self.rects["bottom"].center,self.tilemap.get_colliders(),(0,-1),abs(self.velocity[1])):
                self.velocity[1] = 0
        
        self.tilemap.offset = (self.tilemap.offset[0], self.tilemap.offset[1] + self.velocity[1])
        self.x += self.velocity[0]
        for bullet in self.bullets:
            bullet.update()

    def shoot(self,mouse_pos,power):
        if self.bullet_count > 0:
            self.sounds["gunshot"].play()
            self.bullet_count -= 1
            angle = math.atan2(mouse_pos[1]-self.rect.centery,mouse_pos[0]-self.rect.centerx)
            self.velocity[0] = math.cos(angle)*power
            self.velocity[1] = math.sin(angle)*power
            self.bullets.add(Bullet(self.tilemap,self,Vector2(math.cos(angle)*power,-math.sin(angle)*power),power))



class Bullet(pygame.sprite.Sprite):
    def __init__(self,tile_map,player,velocity,power):
        super().__init__()
        self.tile_map = tile_map
        self.player = player
        self.velocity = velocity
        self.power = power
        self.image = pygame.surface.Surface((2,2))
        self.rect = self.image.get_rect(center=player.rect.center)
        self.image.fill((255,255,0))

    def update(self):
        self.rect.move_ip(self.velocity[0],self.velocity[1])
        colliders = self.tile_map.get_colliders()
        interactibles = self.tile_map.get_interactibles()
        interactiblecollision = self.rect.collidelist(interactibles)

        if self.rect.bottom >= self.tile_map.height*16:
            self.player.bullets.remove(self)
        elif self.rect.bottom <= 0:
            self.player.bullets.remove(self)
        elif self.rect.right >= self.tile_map.width*16:
            self.player.bullets.remove(self)
        elif self.rect.x <= 0:
            self.player.bullets.remove(self)
        elif self.rect.collidelist(colliders) != -1:
            self.player.bullets.remove(self)

def display_to_map_coords(tile_map,x,y):
    return ((x+tile_map.offset[0])//16,(y+tile_map.offset[1])//16)

def raycast(origin,colliders,direction,length):
    for i in range(0,round(length+0.5),1):
        for collider in colliders:
            if collider.collidepoint(origin[0]+direction[0]*i,origin[1]+direction[1]*i):
                return collider
    return None

if __name__ == "__main__":
    import pygame
    from tiles import Tilemap, TileSet
    
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    tile_set = TileSet(".\\tiled_map\\terrain.png", 16)
    tile_map = Tilemap(".\\tiled_map\\map", tile_set)
    player = Player((960, 540), tile_map)
    clock = pygame.time.Clock()
    playing = True
    font = pygame.font.SysFont("Segoe UI", 30)

    while playing:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    playing = False
                if event.key == pygame.K_w:
                    player.velocity[1] = 5
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot(pygame.mouse.get_pos(),player.power)
        screen.fill((33,31,48))
        tile_map.draw(screen)
        player.update()
        player.draw(screen)
        textsurface = font.render(str(tile_map.offset), True, (255, 255, 255))
        screen.blit(textsurface, (0,0))
        pygame.display.flip()
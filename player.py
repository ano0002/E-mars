import pygame,math

class Player():
    def __init__(self) -> None:
        self.image = pygame.transform.scale(pygame.image.load('player.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 100
        self.velocity = [0, 0]
        self.gravity = 0.5
        self.gun = pygame.transform.scale(pygame.image.load('gun.png'), (25, 25))
        self.max_bullets = 2
        self.bullets = self.max_bullets
    def update(self):
        self.rect.move_ip(self.velocity)
        self.velocity[0] = round(self.velocity[0] * 0.9,3)
        if not self.rect.bottom>=600:
            self.velocity[1] += self.gravity
        else:
            self.rect.bottom = 600
            self.velocity[1] = 0
            self.bullets = self.max_bullets
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pos = pygame.mouse.get_pos()
        angle = 360-math.atan2(pos[1]-self.rect.centery,pos[0]-self.rect.centerx)*180/math.pi
        rotimage = pygame.transform.rotate(self.gun,angle)
        rect = rotimage.get_rect(center=self.rect.center)
        screen.blit(rotimage, rect)
        
    def shoot(self,mouse_pos,power):
        if self.bullets>0:
            self.bullets -= 1
        else:
            return
        angle = math.radians(360-math.atan2(mouse_pos[1]-self.rect.centery,mouse_pos[0]-self.rect.centerx)*180/math.pi)
        self.velocity[0] = -math.cos(angle)*power
        self.velocity[1] = math.sin(angle)*power
        self.rect.move_ip(self.velocity)
        
        

if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((800, 600))
    player = Player()
    clock = pygame.time.Clock()
    
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
        player.update()
        display.fill((0,0,0))
        player.draw(display)
        pygame.display.update()
        clock.tick(60)
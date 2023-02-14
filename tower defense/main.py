import pygame
from pygame.locals import *
from ennemy import Ennemy, EnnemyManager, Wave
from terrain import Terrain
from ui import Button,Text
from tower import Turret, LaserTurret, PlaceHolder


class Game():
    def __init__(self):
        pygame.init()
        self.terrain = Terrain("./tiled_map/map.csv")
        self.spawner = EnnemyManager(self.terrain)
        self.buttons = pygame.sprite.Group()
        self.turrets = pygame.sprite.Group()
        self.ennemies = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()
        self.display = pygame.display.set_mode((712,288))
        self.placeholder = None
        self.buttons.add(Button(512,0,200,50,text="Laser Turret : 100",on_click=self.new_turret))
        self.buttons.add(Button(512,50,200,50,text="Next Wave",on_click=self.next_wave))
        self.clock = pygame.time.Clock()
        self.money_text = Text(512,100,"Money : ",font_size = 30,text_color=(255,255,255))
        self.texts.add(self.money_text)
        self.money = 200
        self.particles = []
        self.lives_text = Text(512,130,"   ♥",font_size = 30,text_color=(255,255,255))
        self.texts.add(self.lives_text)
        self.lives = 100
        
    @property
    def money(self):
        return self._money
    
    @money.setter
    def money(self,value):
        self._money = value
        self.money_text.text = "Money : {}".format(self.money)
    @property
    def lives(self):
        return self._lives
    
    @lives.setter
    def lives(self,value):
        self._lives = value
        self.lives_text.text = "{}♥".format(str(self.lives).zfill(3))
        
        
    def new_turret(self,button,mousepos):
        self.unselect_all()
        self.placeholder = PlaceHolder(*mousepos,self.terrain,LaserTurret)
        self.buttons.add(self.placeholder)

    def next_wave(self,button,mousepos):
        self.generate_new_wave()
        self.spawner.next_wave()

    def unselect_all(self):
        for turret in self.turrets:
            turret.selected = False

    def generate_new_wave(self):
        self.spawner.add_round([Wave(10,16,1,1,1,(255,0,0),self.terrain)])

    def hit(self,damage):
        self.lives -= damage
        if self.lives <= 0:
            print("Game Over")
            pygame.quit()
            quit()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                            unselect = True
                            for button in self.buttons:
                                if button.rect.collidepoint(event.pos):
                                    button.on_click(button,mousepos=event.pos)
                                    unselect = False
                            for turret in self.turrets:
                                if turret.rect.collidepoint(event.pos):
                                    turret.on_click(turret,mousepos=event.pos)
                                    unselect = False
                            if unselect:
                                self.unselect_all()
            self.display.fill((0,0,0))
            self.terrain.draw(self.display)
            self.spawner.update()
            self.spawner.draw(self.display)
            self.buttons.update(pygame.mouse.get_pos())
            self.buttons.draw(self.display)
            self.turrets.update()
            self.turrets.draw(self.display)
            self.texts.draw(self.display)
            
            for turret in self.turrets:
                if turret.selected:
                    pygame.draw.circle(self.display, (255,0,0), turret.rect.center, turret.range, 3)
            
            if self.placeholder : 
                self.placeholder.update(pygame.mouse.get_pos())
                self.placeholder.draw(self.display)
            
            for particle in self.particles:
                particle.update()
                particle.draw(self.display)
                if not particle.alive:
                    self.particles.remove(particle)
                    del particle
            
            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.run()  
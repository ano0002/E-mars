import pygame

class Button(pygame.sprite.Sprite):
    default_on_click = lambda self,mousepos: print("Clicked")
    
    def __init__(self, x, y, width, height, color=(255,255,255), text="", text_color=(0,0,0), font_size=30,on_click=None):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text_color = text_color
        self.font_size = font_size
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.text = text
        if on_click:
            self.on_click = on_click
        else:
            self.on_click = self.default_on_click  
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
        self.text_image = self.font.render(value, True, self.text_color)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = (self.rect.width/2, self.rect.height/2)
        self.image.blit(self.text_image, self.text_rect)
        
      
    def update(self, mousepos):
        if self.rect.collidepoint(mousepos):
            self.image.fill((200,200,200))
        else:
            self.image.fill((255,255,255))
        self.image.blit(self.text_image, self.text_rect)
    
        
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Button")
    display = pygame.display.set_mode((800, 600))
    buttons = pygame.sprite.Group()
    
    def func(button, mousepos):
        if button.text == "Test":
            button.text = "Clicked"
        else:
            button.text = "Test"
    
    for i in range(10):
        buttons.add(Button(100, 50*i+10*i+5, 100, 50, text="Test",on_click=func))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                        for button in buttons:
                            if button.rect.collidepoint(event.pos):
                                button.on_click(button,mousepos=event.pos)
        display.fill((0,0,0))
        buttons.update(pygame.mouse.get_pos())
        buttons.draw(display)
        pygame.display.update()
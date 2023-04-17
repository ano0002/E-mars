import pygame


 
COULEURS = {
    'white': (255,255,255),
    'black': (0,0,0),
    'red': (255,0,0),
    'green': (0,255,0),
    'blue': (0,0,255),
    'yellow': (255,255,0),
    }


pygame.init()
pygame.font.init()
 
RUNNING = True
 
fenetre = pygame.display.set_mode((500,500))
myfont = pygame.font.SysFont('Helvetic', 20)
 
 
def gerer_events_principale():
    global RUNNING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
 
def menu():
    rect = pygame.draw.rect(
        fenetre,
        (255,0,0), pygame.Rect(100, 200, 100, 100))
    text = myfont.render('Bubble Shoot', False, (255,255,255))
    fenetre.blit(text, (100,200))
 
    gerer_mouse_menu(rect)
     
#def jeu():
#    rect = pygame.draw.rect(
#        fenetre,
#        (0,255,0),
#        pygame.Rect(100, 200, 100, 100))
#    text = myfont.render('ButtonB', False, (255,255,255))
#    fenetre.blit(text, (100,200))
#    gerer_mouse_jeu(rect)
     
def gerer_mouse_jeu(rectangle):
    global afficher
     
    mouse = pygame.mouse.get_pressed()
    if mouse[0]: # UP
        mouse_pos = pygame.mouse.get_pos()
         
        if rectangle.collidepoint(mouse_pos):
            print('Cliqué sur:', rectangle)
            afficher = menu
 
def gerer_mouse_menu(rectangle):
    global afficher
     
    mouse = pygame.mouse.get_pressed()
    if mouse[0]: # UP
        mouse_pos = pygame.mouse.get_pos()
         
        if rectangle.collidepoint(mouse_pos):
            print('Cliqué sur:', rectangle)
            pygame.time.wait(500)
            import bubbleshoot
 
## Affecte la fonction menu
afficher = menu
 
def boucle_principale():
    while RUNNING:
        fenetre.fill( (0,0,0) )
         
        gerer_events_principale()
         
        ## Exécute la fonction affecté à afficher (menu/jeu)
        afficher()
         
         
        pygame.display.update()
         
    pygame.quit()
 
 
 
boucle_principale()
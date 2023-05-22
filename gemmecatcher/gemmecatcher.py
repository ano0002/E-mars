
import pygame
import random
def gemmecatcher(screen_size,screen,delta_time):

    # Set the title of the game window
    pygame.display.set_caption("Bubble Shooter")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Load the background image
    background_image = pygame.transform.scale(pygame.image.load(".\\gemmecatcher\\map_cave.jpg"),(screen_size))


    # Load the bubble image
    bubble_image = pygame.transform.scale(pygame.image.load('.\\gemmecatcher\\gemme_python.png'),(20, 30))

    # Define the bubble class
    class Bubble:
        def __init__(self, x, y, size):
            self.x = x
            self.y = y
            self.size = size

        def update(self):
            # Move the bubble down
            self.y += 25 - len(bubble_list)/5

            # If the bubble goes off the bottom of the screen, reset it to the top
            if self.y > screen_size[1]:
                self.y = 0
                self.x = random.randint(0, screen_size[0])

        def draw(self, screen):
            # Draw the bubble image
            screen.blit(bubble_image, (self.x, self.y))


    # Load the cannon image
    cannon_image = pygame.transform.scale(pygame.image.load(".\\gemmecatcher\\player_tube.png").convert_alpha(),(70,2160))
    cannon_width = cannon_image.get_width()


    # Define the cannon class
    class Cannon:
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self, mouse_x, mouse_y):
            # Set the cannon position to the mouse position
            self.rect.topright = (mouse_x, mouse_y)

        def draw(self, screen):
            screen.blit(self.image, self.rect)


    # Create a list of bubbles
    bubble_list = []
    for i in range(100):
        x = random.randint(0, screen_size[0])
        y = random.randint(0, screen_size[1])
        size = 50
        bubble = Bubble(x, y, size)
        bubble_list.append(bubble)

    # Create a cannon
    #cannon = Cannon(0, 0, 50, 50)
    cannon = Cannon(0, 0, cannon_image)

    # Game loop
    running = True
    cannon_color=(0,0,0)
    cannon_color_chage_time=0

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Update and draw the bubbles
        for bubble in bubble_list:
            bubble.update()
            bubble.draw(screen)
            offset=40

            if cannon.rect.x + offset - cannon_width < bubble.x < cannon.rect.x + offset and cannon.rect.y < bubble.y < cannon.rect.y + offset:
                bubble_list.remove(bubble)
                cannon_color = (255, 255, 255)
                cannon_color_change_time = pygame.time.get_ticks()






        # Check if it's time to change the cannon back to its original color
        if cannon_color != (0, 0, 0) and pygame.time.get_ticks() - cannon_color_change_time >= 3000:
            cannon_color = (0, 0, 0)

        # Update the cannon color
        cannon.color = cannon_color

        # Update and draw the cannon
        cannon.update(mouse_x, mouse_y)
        cannon.draw(screen)

        # Check if all the bubbles have been popped
        if len(bubble_list) == 0:
            font = pygame.font.Font(None, 36)
            text = font.render("You won!", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (screen_size[0] // 2, screen_size[1] // 2)
            screen.blit(text, text_rect)
            return delta_time
            
        # Update the screen
        pygame.display.update()

        # Set the frame rate
        clock.tick(60)

    # Quit the game
    return delta_time




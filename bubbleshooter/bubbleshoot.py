import pygame
import random
import time
from typing import List, Tuple
# Initialize Pygame
class Cannon:
    def __init__(self, x:int, y:int, width:int, height:int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self, mouse_x:int, mouse_y:int) -> None:
        # Set the cannon position to the mouse position
        self.x = mouse_x
        self.y = mouse_y

    def draw(self, screen:pygame.display) -> None:
        pygame.draw.rect(screen, (0, 0, 0), (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))


def bubble_shooter(screen_size:Tuple[int,int],screen:pygame.display) -> Tuple[bool, int]:
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Set the screen background color
    background_color = (255, 255, 255)
    start_time = int(time.time())

    class Bubble:
        def __init__(self, x:int, y:int, color:Tuple[int,int,int], size:int) -> None:
            self.x = x
            self.y = y
            self.color = color
            self.size = size

        def update(self) -> None:
            # Move the bubble down
            self.y += 5

            # If the bubble goes off the bottom of the screen, reset it to the top
            if self.y > screen_size[1]:
                self.y = 0
                self.x = random.randint(0, screen_size[0])

        def draw(self, screen:pygame.display) -> None:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)



    # Create a list of bubbles
    bubble_list = []
    size = 5
    for _ in range(50):
        x = random.randint(0, screen_size[0])
        y = random.randint(0, screen_size[1])
        color = (255, 0, 0)
        bubble = Bubble(x, y, color, size)
        bubble_list.append(bubble)

    # Create a cannon
    cannon = Cannon(0, 0, 20, 20)




    # Game loop
    running = True
    cannon_color=(0,0,0)
    cannon_color_chage_time=0

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(background_color)

        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()


        # Update and draw the bubbles
        for bubble in bubble_list:
            bubble.update()
            bubble.draw(screen)

            # Check if the cannon collides with the bubble
            if cannon.x - cannon.width / 2 < bubble.x < cannon.x + cannon.width / 2 and cannon.y - cannon.height / 2 < bubble.y < cannon.y + cannon.height / 2:
                bubble_list.remove(bubble)
                cannon.color = (255, 255, 255)
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
        if not bubble_list:
            font = pygame.font.Font(None, 36)
            text = font.render("You Win!", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (screen_size[0] // 2, screen_size[1] // 2)
            screen.blit(text, text_rect)
            pygame.display.update()
            # wait 3 seconds and then quit
            end_time = int(time.time())
            #difference in seconds
            difference = end_time - start_time
            for _ in range(60 * 3):
                clock.tick(60)
                cannon.update(mouse_x, mouse_y)
                cannon.draw(screen)
            return True, difference

        # Update the screen
        pygame.display.update()

        # Set the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()



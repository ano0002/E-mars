"""
Main Module
"""
import time
import pygame
# from pprint import pprint
from .sprites import GameMovingSprite
from .sprites import UserControlledGameMovingSprite
from .sprites import Ball
from .sprites import Player
from .sprites import Bricks
from .sprites import BreakableBrick
from .collision_handler_sprites import CollisionHandlerSprites
from .collision_handler import CollisionHandler
from .event_dispatcher import EventDispatcher
from .common import Common
from .score import Score

def create_bricks(from_height: int, brick_map: list, screen: pygame.Surface,
                  screen_width: int, screen_height: int,
                  collision_handler: CollisionHandler):
    height: int = screen_height - from_height
    brick_width: int = screen_width / len(brick_map[0])
    brick_height: int = 3 * height / (4 * len(brick_map))
    breakable_brick_positions: list = []
    index_x: int = 0
    index_y: int = 0
    for row in brick_map:
        for element in row:
            if element != ' ':
                position = {'x':index_x * brick_width + brick_width // 2,
                            'y':index_y * brick_height + brick_height // 2 + from_height}
            if element == 'X':
                breakable_brick_positions.append(position)
            index_x += 1
        index_y += 1
        index_x = 0

    bricks = [BreakableBrick(screen)\
        .set_image(brick_width, brick_height, Common.BRICK_IMAGE_NAME)\
            .set_position(pos['x'], pos['y'])\
                .set_collision_handler(collision_handler)\
                    for pos in breakable_brick_positions]
    return bricks

def wallbreaker(screen,screen_size, time_delta):
    start_time = time.time()
    screen_width: int = 1000
    screen_height: int = 800
    from_height: int = 50
    pygame.init()
    screen_width, screen_height = screen_size

    brick_map = ["  XXXXX   XXX",
                 "    XXXXXXXXX",
                 "XX         XX",
                 "XX         XX",
                 "XX  XXXXXXXXX",
                 "   XX        ",
                 "XX  XX    XX ",
                 "XX   XX   XX ",
                 "XX    XX     ",
                 "       XX    ",
                 "XX      XX   "]

    pygame.display.set_caption('Wall breaker')
    score_height = 80
    score: Score = Score(screen, score_height)
    finish = Bricks()
    collision_handler: CollisionHandler = CollisionHandlerSprites(score)
    ball: GameMovingSprite = Ball(screen)\
        .set_image(10, 10, Common.BALL_IMAGE_NAME)\
            .set_position(screen_width // 2, 4 * screen_height // 5)\
                .set_collision_handler(collision_handler)
    player: UserControlledGameMovingSprite = Player(screen)\
        .set_image(90, 72, Common.PING_IMAGE_NAME)\
            .set_position(screen_width // 2, screen_height - 36)\
                .set_collision_handler(collision_handler)
    event_dispatcher: EventDispatcher = EventDispatcher()
    event_dispatcher.subscribe(player)
    collision_handler.subscribe_moving(player)
    collision_handler.subscribe_moving(ball)
    bricks = create_bricks(from_height, brick_map, screen, screen_width, screen_height, collision_handler)
    for brick in bricks:
        collision_handler.subscribe_static(brick)

    clock: pygame.time.Clock = pygame.time.Clock()

    bubble = pygame.image.load("./set_bubbles/4_wallbreacker.png")
    is_bubble = True
    while not event_dispatcher.is_done() and finish.breaked < 5:
        if is_bubble:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    is_bubble = False
                    start_time = time.time()
        else:
            event_dispatcher.process_event()
            player.move()
            ball.move()
        screen.fill(Common.BLACK)
        player.display_on_screen()
        ball.display_on_screen()
        for brick in bricks:
            brick.display_on_screen()
        if sum([brick.number_remaining_bumps+1 for brick in bricks]) == 0:
             return time_delta + time.time() - start_time
        if is_bubble:
            screen.blit(bubble,(screen_size[0]/2-bubble.get_width()/2,screen_size[1]-bubble.get_height()))
        else :
            time_elapsed = round(time_delta + time.time() - start_time,3)
            time_text = pygame.font.SysFont('Consolas', 30).render(str(time_elapsed), False, (255, 255, 255))
            screen.blit(time_text,(screen_size[0]/2,0))
        pygame.display.flip()
        clock.tick(80)

        
    exit()

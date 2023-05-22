import pygame
from wall.sprites import GameMovingSprite
from wall.sprites import UserControlledGameMovingSprite
from wall.sprites import Ball
from wall.sprites import Player
from wall.sprites import Bricks
from wall.sprites import BreakableBrick
from wall.collision_handler_sprites import CollisionHandlerSprites
from wall.collision_handler import CollisionHandler
from wall.event_dispatcher import EventDispatcher
from wall.common import Common
from wall.score import Score

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

def start():
    screen_width: int = 1000
    screen_height: int = 800
    from_height: int = 50
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height),
                                     pygame.FULLSCREEN | pygame.DOUBLEBUF )
    screen_width, screen_height = screen.get_size()
    background_image = pygame.transform.scale(pygame.image.load("map_cave.jpg"), (screen_width, screen_height))
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

    while not event_dispatcher.is_done() and finish.breaked < 5:
        event_dispatcher.process_event()
        player.move()
        ball.move()
        screen.blit(background_image, (0, 0))
        player.display_on_screen()
        ball.display_on_screen()
        score.display_on_screen()
        for brick in bricks:
            brick.display_on_screen()

        pygame.display.flip()
        clock.tick(80)
    pygame.quit()
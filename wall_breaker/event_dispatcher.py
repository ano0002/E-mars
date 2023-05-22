import pygame
from .sprites import GameMovingSprite

class EventDispatcher():
    is_done_status: bool = False
    controlled_moving_sprites: list = []

    def subscribe(self, controlled_moving_sprite: GameMovingSprite) -> None:
        self.controlled_moving_sprites.append(controlled_moving_sprite)

    def unsubscribe(self, controlled_moving_sprite: GameMovingSprite) -> None:
        self.controlled_moving_sprites.remove(controlled_moving_sprite)

    def process_event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_done_status = True

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.is_done_status = True

                for controlled_moving_sprite in self.controlled_moving_sprites:
                    controlled_moving_sprite.start_direction(event.key)

            if event.type == pygame.KEYUP:
                for controlled_moving_sprite in self.controlled_moving_sprites:
                    controlled_moving_sprite.stop_direction(event.key)

            if event.type == pygame.MOUSEMOTION:
                for controlled_moving_sprite in self.controlled_moving_sprites:
                    controlled_moving_sprite.mouse_position_move(pygame.mouse.get_pos())

    def is_done(self) -> bool:
        return self.is_done_status
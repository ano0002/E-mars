from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple
from dataclasses import dataclass
import pygame
from wall.collision_handler import CollisionHandler

@dataclass
class Image:
    image: pygame.Surface = None
    width: int = 0
    height: int = 0
    perimeter: list(dict) = None
    rect: pygame.Rect = None


@dataclass
class Display:
    screen: pygame.Surface = None
    screen_width: int = 0
    screen_height: int = 0

class StaticSprite(pygame.sprite.Sprite, ABC):
    collision_handler: CollisionHandler = None
    display: Display = None
    image: Image = None

    def __init__(self, screen: pygame.Surface):
        super().__init__()
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.display = Display(screen, screen_width, screen_height)

    def set_collision_handler(self, collision_handler: CollisionHandler) -> StaticSprite:
        self.collision_handler = collision_handler
        return self

    def set_image(self, width: int, height: int,
                  image_path: str) -> StaticSprite:
        if self.image is not None and self.image.rect is not None:
            self.image.rect.x += self.image.width // 2
            self.image.rect.y += self.image.height // 2

        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        perimeter = [{'x': 0, 'y': 0}, {'x': width, 'y': height}]
        self.image = Image(image, width, height, perimeter,
                           image.get_rect())

        self.set_position(self.image.rect.x, self.image.rect.y)
        return self

    def set_position(self, pos_x: int, pos_y: int) -> StaticSprite:
        if self.image is not None and self.image.rect is not None:
            self.image.rect.x = pos_x - self.image.width // 2
            self.image.rect.y = pos_y - self.image.height // 2
        else:
            print("Error trying to set a position on an image "
                  "that does not exist yet! Set the image first!")
        return self

    def display_on_screen(self) -> None:
        self.display.screen.blit(self.image.image, (self.image.rect.x,self.image.rect.y))

    def get_perimeter(self) -> list({}):
        return self.image.perimeter

    def get_perimeter_optimized(self) -> list({}):
        return self.image.perimeter

    def get_position(self) -> Tuple[int, int]:
        return (self.image.rect.x, self.image.rect.y)

    def get_position_for_collision_analysis(self) -> Tuple[int, int]:
        return self.get_position()

    @abstractmethod
    def bumped(self, from_side_bumped: dict) -> None:
        """
        Inform that this sprite bumbed or was bumped
        """
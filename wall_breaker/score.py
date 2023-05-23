from typing import Tuple
import pygame
from .static_sprite import Display

class Score(pygame.sprite.Sprite):
    font: pygame.font = None
    score: int = -10
    green: Tuple[int, int, int] = (0, 255, 0)
    blue: Tuple[int, int, int] = (0, 0, 255)
    display: Display = None
    height = 0

    def __init__(self, screen: pygame.Surface, height: int):
        super().__init__()
        pygame.font.init()
        self.font: pygame.Font = pygame.font.SysFont('Comic Sans MS', 30)
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.display = Display(screen, screen_width, screen_height)
        self.height = height

    def add_score(self, added_score) -> None:
        self.score += added_score

    def get_score_images(self):
        color_score: Tuple[int, int, int] = self.green
        text_surface = self.font.render('Your score: ', False, self.blue)
        score_surface = self.font.render(str(self.score), False, color_score)
        return text_surface, score_surface

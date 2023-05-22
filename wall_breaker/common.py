"""
All commons are here
"""
from dataclasses import dataclass


@dataclass
class Common:
    """
    Define constants
    """
    BLACK = (0, 0, 0)
    BALL_IMAGE_NAME = './wall_breaker/ball.png'
    PING_IMAGE_NAME = './wall_breaker/astro_shield.png'
    BRICK_IMAGE_NAME = './wall_breaker/brick.png'
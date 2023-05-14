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
    BALL_IMAGE_NAME = 'ball.png'
    PING_IMAGE_NAME = 'astro_shield.png'
    BRICK_IMAGE_NAME = 'brick.png'
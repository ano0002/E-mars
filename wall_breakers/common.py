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
    BALL_IMAGE_NAME = 'Brick.png'
    PING_IMAGE_NAME = 'Brick.png'
    BRICK_IMAGE_NAME = 'Brick.png'
    UNBREAKABLE_BRICK_IMAGE_NAME = 'Brick.png'
    POISONED_BRICK_IMAGE_NAME = 'Brick.png'
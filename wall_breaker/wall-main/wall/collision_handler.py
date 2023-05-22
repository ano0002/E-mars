from abc import ABC, abstractmethod
from typing import Tuple

class CollisionHandler(ABC):
    LEFT = 'left'
    RIGHT = 'right'
    TOP = 'top'
    BOTTOM = 'bottom'
    NONE = 'none'
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'

    def __init__(self):
        """"""

    @abstractmethod
    def vertical_collision_side_bumped(self, from_side_bumped: dict) -> Tuple[bool, int]:
        """"""

    @abstractmethod
    def horizontal_collision_side_bumped(self, from_side_bumped: dict) -> Tuple[bool, int]:
        """"""

    @abstractmethod
    def inform_sprite_about_to_move(self) -> None:
        """"""

    @abstractmethod
    def unsubscribe(self, sprite) -> None:
        """"""

    @abstractmethod
    def add_score(self, score_add: int) -> None:
        """"""
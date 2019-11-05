from enum import Enum
from .Point import Point


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


DIRECTION_POINT = {
    Direction.RIGHT: Point(1, 0),
    Direction.LEFT: Point(-1, 0),
    Direction.UP: Point(0, -1),
    Direction.DOWN: Point(0, 1)
}

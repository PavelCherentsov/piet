from enum import Enum


class DirectionPointer:
    def __init__(self):
        self.direction = Direction.RIGHT

    def pointer(self, k):
        self.direction = Direction((self.direction.value + k) % 4)


class CodelChooser:
    def __init__(self):
        self.direction = Direction.LEFT

    def switch(self, k):
        if k % 2 != 0:
            if self.direction == Direction.RIGHT:
                self.direction = Direction.LEFT
            else:
                self.direction = Direction.RIGHT


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class Point:
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color
        self.is_used = False
        self.is_stop = False

    def __rmul__(self, other):
        return Point(other * self.x, other * self.y, self.color)


DIRECTION_POINT = {
    Direction.RIGHT: Point(1, 0),
    Direction.LEFT: Point(-1, 0),
    Direction.UP: Point(0, -1),
    Direction.DOWN: Point(0, 1)
}

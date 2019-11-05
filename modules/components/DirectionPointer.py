from .Direction import Direction


class DirectionPointer:
    def __init__(self):
        self.direction = Direction.RIGHT

    def pointer(self, k):
        self.direction = Direction((self.direction.value + k) % 4)

from .Direction import Direction


class DirectionPointer:
    def __init__(self):
        self.direction = Direction[0]

    def pointer(self, k):
        while k < 0:
            k += 4
        self.direction = Direction(k // 4)

from .Direction import Direction


class CodelChooser:
    def __init__(self):
        self.direction = Direction.LEFT

    def switch(self, k):
        if k % 2 != 0:
            if self.direction == Direction.RIGHT:
                self.direction = Direction.LEFT
            else:
                self.direction = Direction.RIGHT


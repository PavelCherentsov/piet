from .Direction import Direction


class CodelChooser:
    def __init__(self):
        self.direction = Direction[2]

    def switch(self, k):
        if k // 2 != 0:
            if self.direction == Direction[0]:
                self.direction = Direction[2]
            else:
                self.direction = Direction[0]

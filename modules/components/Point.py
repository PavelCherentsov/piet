class Point:
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color
        self.is_used = False
        self.is_stop = False

    def __rmul__(self, other):
        return Point(other * self.x, other * self.y, self.color)

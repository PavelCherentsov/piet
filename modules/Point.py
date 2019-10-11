class Point:
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color
        self.is_used = False

    def __rmul__(self, other):
        return Point(other * self.x, other * self.y, self.color)

    def __str__(self):
        return "Point: ({},{}): color: {}".format(self.x,
                                                 self.y,
                                                 self.color)

class Point:
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color
        self.isUsed = False

    def __str__(self):
        return "Point({}, {}) - {} / {}".format(self.x, self.y, self.color, self.isUsed)



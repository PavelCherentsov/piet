from .CodelChooser import CodelChooser
from .DirectionPointer import DirectionPointer

directionPoints = [(1, 0), (-1, 0), (0, 1), (0, -1)]

class Interpreter:
    def __init__(self, image):
        self.x = 1
        self.y = 1
        self.direction_pointer = DirectionPointer()
        self.codel_chooser = CodelChooser()
        self.points = image
        self.previos = None
        self.stack = []
        self.block = []
        self.initialize_block()

    def initialize_block(self):
        color = self.points[self.x][self.y].color
        self.block = []
        self.stack.append(self.points[self.x][self.y])
        self.points[self.x][self.y].isUsed = True
        self.block.append(self.points[self.x][self.y])
        while len(self.stack) != 0:
            point = self.stack.pop()
            for dp in directionPoints:
                p = self.points[point.x + dp[0]][point.y + dp[1]]
                if p.color == color:
                    if not p.isUsed:
                        p.isUsed = True
                        self.stack.append(p)
                        self.block.append(p)

        self.previos = len(self.block)
        for e in self.block:
            e.isUsed = False

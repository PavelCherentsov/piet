from .CodelChooser import CodelChooser
from .DirectionPointer import DirectionPointer
from .Direction import Direction
from .Point import Point
from math import inf

directionPoints = [(1, 0), (-1, 0), (0, 1), (0, -1)]

class Interpreter:
    def __init__(self, image):
        self.x = 1
        self.y = 1
        self.direction_pointer = DirectionPointer()
        self.codel_chooser = CodelChooser()
        self.points = image
        self.previous_value = None
        self.previous_color = None
        self.stack = []
        self.block = []
        self.direction_pointer.direction=Direction[3]
        self.codel_chooser.direction = Direction[0]
        self.initialize_block()
        self.init_next_pixel()

    def initialize_block(self):
        self.previous_color = self.points[self.x][self.y].color
        self.block = []
        self.stack.append(self.points[self.x][self.y])
        self.points[self.x][self.y].isUsed = True
        self.block.append(self.points[self.x][self.y])
        while len(self.stack) != 0:
            point = self.stack.pop()
            for dp in directionPoints:
                p = self.points[point.x + dp[0]][point.y + dp[1]]
                if p.color == self.previous_color:
                    if not p.isUsed:
                        p.isUsed = True
                        self.stack.append(p)
                        self.block.append(p)

        self.previous_value = len(self.block)
        for e in self.block:
            e.isUsed = False

    def next(self):
        pass

    def init_next_pixel(self):
        if self.direction_pointer.direction == Direction[0]:
            if self.codel_chooser.direction == Direction[2]:
                best = inf
                best_p = Point(-inf, -inf, None)
                for p in self.block:
                    if p.y < best:
                        best = p.y
            if self.codel_chooser.direction == Direction[0]:
                best = -inf
                best_p = Point(-inf, -inf, None)
                for p in self.block:
                    if p.y > best:
                        best = p.y
            for p in self.block:
                if p.y == best:
                    if p.x > best_p.x:
                        best_p = p
        if self.direction_pointer.direction == Direction[1]:
            if self.codel_chooser.direction == Direction[2]:
                best = -inf
                best_p = Point(inf, -inf, None)
                for p in self.block:
                    if p.x > best:
                        best = p.x
            if self.codel_chooser.direction == Direction[0]:
                best = inf
                best_p = Point(inf, -inf, None)
                for p in self.block:
                    if p.x < best:
                        best = p.x
            for p in self.block:
                if p.x == best:
                    if p.y > best_p.y:
                        best_p = p
        if self.direction_pointer.direction == Direction[2]:
            if self.codel_chooser.direction == Direction[0]:
                best = inf
                best_p = Point(inf, -inf, None)
                for p in self.block:
                    if p.y < best:
                        best = p.y
            if self.codel_chooser.direction == Direction[2]:
                best = -inf
                best_p = Point(inf, -inf, None)
                for p in self.block:
                    if p.y > best:
                        best = p.y
            for p in self.block:
                if p.y == best:
                    if p.x < best_p.x:
                        best_p = p
        if self.direction_pointer.direction == Direction[3]:
            if self.codel_chooser.direction == Direction[2]:
                best = inf
                best_p = Point(inf, inf, None)
                for p in self.block:
                    if p.x < best:
                        best = p.x
            if self.codel_chooser.direction == Direction[0]:
                best = -inf
                best_p = Point(inf, inf, None)
                for p in self.block:
                    if p.x > best:
                        best = p.x
            for p in self.block:
                if p.x == best:
                    if p.y < best_p.y:
                        best_p = p
        print(best_p)



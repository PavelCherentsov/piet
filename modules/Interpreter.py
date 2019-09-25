from math import inf
import sys

from .CodelChooser import CodelChooser
from .Direction import Direction
from .DirectionPointer import DirectionPointer
from .Point import Point
from .ColorTable import get_command
from .Stack import Stack

directionPoints = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Interpreter:
    def __init__(self, image, x, y):
        self.x = x
        self.y = y
        self.direction_pointer = DirectionPointer()
        self.codel_chooser = CodelChooser()
        self.points = image
        self.previous_value = None
        self.previous_color = None
        self.stack = Stack()
        self.block = []
        while True:
            start_white = []
            self.initialize_block()
            k = 0
            while k != 8:
                next_pixel = self.init_next_pixel()
                if next_pixel.color == 'black':
                    k += 1
                    self.codel_chooser.switch(1)
                    next_pixel = self.init_next_pixel()
                    if next_pixel.color == 'black':
                        self.direction_pointer.pointer(1)
                        k += 1
                    else:
                        break
                else:
                    break
            if k == 8:
                sys.exit(0)
            if next_pixel.color == 'white':
                while next_pixel.color == 'white':
                    if self.direction_pointer.direction == Direction[0]:
                        if self.points[next_pixel.x + 1][next_pixel.y].color == 'black':
                            self.direction_pointer.pointer(1)
                            self.codel_chooser.switch(1)
                        else:
                            start_white.append(next_pixel)
                            next_pixel = self.points[next_pixel.x + 1][next_pixel.y]
                    elif self.direction_pointer.direction == Direction[1]:
                        if self.points[next_pixel.x][next_pixel.y+1].color == 'black':
                            self.direction_pointer.pointer(1)
                            self.codel_chooser.switch(1)
                        else:
                            start_white.append(next_pixel)
                            next_pixel = self.points[next_pixel.x][next_pixel.y + 1]
                    elif self.direction_pointer.direction == Direction[2]:
                        if self.points[next_pixel.x - 1][next_pixel.y].color == 'black':
                            self.direction_pointer.pointer(1)
                            self.codel_chooser.switch(1)
                        else:
                            start_white.append(next_pixel)
                            next_pixel = self.points[next_pixel.x - 1][next_pixel.y]
                    elif self.direction_pointer.direction == Direction[3]:
                        if self.points[next_pixel.x][next_pixel.y - 1].color == 'black':
                            self.direction_pointer.pointer(1)
                            self.codel_chooser.switch(1)
                        else:
                            start_white.append(next_pixel)
                            next_pixel = self.points[next_pixel.x][next_pixel.y - 1]
                    if next_pixel in start_white:
                        sys.exit(0)

            self.x = next_pixel.x
            self.y = next_pixel.y
            if start_white == []:
                command = get_command(self.previous_color, next_pixel.color)
                command.__call__(self)

    def initialize_block(self):
        stack = []
        self.previous_color = self.points[self.x][self.y].color
        self.block = []
        stack.append(self.points[self.x][self.y])
        self.points[self.x][self.y].isUsed = True
        self.block.append(self.points[self.x][self.y])
        while len(stack) != 0:
            point = stack.pop()
            for dp in directionPoints:
                p = self.points[point.x + dp[0]][point.y + dp[1]]
                if p.color == self.previous_color:
                    if not p.isUsed:
                        p.isUsed = True
                        stack.append(p)
                        self.block.append(p)

        self.previous_value = len(self.block)
        for e in self.block:
            e.isUsed = False

    def next(self):
        pass

    def init_next_pixel(self):

        if self.direction_pointer.direction == Direction[0]:
            best = -inf
            for p in self.block:
                if p.x > best:
                    best = p.x
            if self.codel_chooser.direction == Direction[2]:
                best_p = Point(best, inf, None)
                for p in self.block:
                    if p.x == best:
                        if p.y < best_p.y:
                            best_p = p
            if self.codel_chooser.direction == Direction[0]:
                best_p = Point(best, -inf, None)
                for p in self.block:
                    if p.x == best:
                        if p.y > best_p.y:
                            best_p = p

        if self.direction_pointer.direction == Direction[1]:
            best = -inf
            for p in self.block:
                if p.y > best:
                    best = p.y
            if self.codel_chooser.direction == Direction[2]:
                best_p = Point(-inf, best, None)
                for p in self.block:
                    if p.y == best:
                        if p.x > best_p.x:
                            best_p = p
            if self.codel_chooser.direction == Direction[0]:
                best_p = Point(inf, best, None)
                for p in self.block:
                    if p.y == best:
                        if p.x < best_p.x:
                            best_p = p

        if self.direction_pointer.direction == Direction[2]:
            best = +inf
            for p in self.block:
                if p.x < best:
                    best = p.x
            if self.codel_chooser.direction == Direction[2]:
                best_p = Point(best, -inf, None)
                for p in self.block:
                    if p.x == best:
                        if p.y > best_p.y:
                            best_p = p
            if self.codel_chooser.direction == Direction[0]:
                best_p = Point(best, inf, None)
                for p in self.block:
                    if p.x == best:
                        if p.y < best_p.y:
                            best_p = p

        if self.direction_pointer.direction == Direction[3]:
            best = +inf
            for p in self.block:
                if p.y < best:
                    best = p.y
            if self.codel_chooser.direction == Direction[2]:
                best_p = Point(+inf, best, None)
                for p in self.block:
                    if p.y == best:
                        if p.x < best_p.x:
                            best_p = p
            if self.codel_chooser.direction == Direction[0]:
                best_p = Point(-inf, best, None)
                for p in self.block:
                    if p.y == best:
                        if p.x > best_p.x:
                            best_p = p

        if self.direction_pointer.direction == Direction[0]:
            return self.points[best_p.x+1][best_p.y]
        if self.direction_pointer.direction == Direction[1]:
            return self.points[best_p.x][best_p.y+1]
        if self.direction_pointer.direction == Direction[2]:
            return self.points[best_p.x-1][best_p.y]
        if self.direction_pointer.direction == Direction[3]:
            return self.points[best_p.x][best_p.y-1]



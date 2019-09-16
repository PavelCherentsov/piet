from .CodelChooser import CodelChooser
from .DirectionPointer import DirectionPointer


class Interpreter:
    def __init__(self, image):
        self.x = 0
        self.y = 0
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
            print(point)
            print(len(self.points[0]) - 1)
            print(len(self.points) - 1)
            if point.x == 0 == point.y:
                p_right = self.points[point.x + 1][point.y]
                p_down = self.points[point.x][point.y + 1]
                if p_right.color == color:
                    if not p_right.isUsed:
                        p_right.isUsed = True
                        self.stack.append(p_right)
                        self.block.append(p_right)
                if p_down.color == color:
                    if not p_down.isUsed:
                        p_down.isUsed = True
                        self.stack.append(p_down)
                        self.block.append(p_down)
            elif point.x == 0 and 0 < point.y < len(self.points[0]) - 1:
                p_right = self.points[point.x + 1][point.y]
                p_down = self.points[point.x][point.y + 1]
                p_up = self.points[point.x][point.y - 1]
                if p_right.color == color:
                    if not p_right.isUsed:
                        p_right.isUsed = True
                        self.stack.append(p_right)
                        self.block.append(p_right)
                if p_down.color == color:
                    if not p_down.isUsed:
                        p_down.isUsed = True
                        self.stack.append(p_down)
                        self.block.append(p_down)
                if p_up.color == color:
                    if not p_up.isUsed:
                        p_up.isUsed = True
                        self.stack.append(p_up)
                        self.block.append(p_up)
            elif point.y == 0 and 0 < point.x < len(self.points)-1:
                p_right = self.points[point.x + 1][point.y]
                p_down = self.points[point.x][point.y + 1]
                p_left = self.points[point.x-1][point.y]
                if p_right.color == color:
                    if not p_right.isUsed:
                        p_right.isUsed = True
                        self.stack.append(p_right)
                        self.block.append(p_right)
                if p_down.color == color:
                    if not p_down.isUsed:
                        p_down.isUsed = True
                        self.stack.append(p_down)
                        self.block.append(p_down)
                if p_left.color == color:
                    if not p_left.isUsed:
                        p_left.isUsed = True
                        self.stack.append(p_left)
                        self.block.append(p_left)
            elif point.y == 0 and point.x == len(self.points)-1:
                p_down = self.points[point.x][point.y + 1]
                p_left = self.points[point.x-1][point.y]
                if p_down.color == color:
                    if not p_down.isUsed:
                        p_down.isUsed = True
                        self.stack.append(p_down)
                        self.block.append(p_down)
                if p_left.color == color:
                    if not p_left.isUsed:
                        p_left.isUsed = True
                        self.stack.append(p_left)
                        self.block.append(p_left)
            elif point.x == 0 and point.y == len(self.points[0]) - 1:
                p_right = self.points[point.x + 1][point.y]
                p_up = self.points[point.x][point.y - 1]
                if p_right.color == color:
                    if not p_right.isUsed:
                        p_right.isUsed = True
                        self.stack.append(p_right)
                        self.block.append(p_right)
                if p_up.color == color:
                    if not p_up.isUsed:
                        p_up.isUsed = True
                        self.stack.append(p_up)
                        self.block.append(p_up)
            elif 0 < point.x < len(self.points) - 1 and point.y == len(self.points[0]) - 1:
                p_right = self.points[point.x + 1][point.y]
                p_up = self.points[point.x][point.y - 1]
                p_left = self.points[point.x - 1][point.y]
                if p_right.color == color:
                    if not p_right.isUsed:
                        p_right.isUsed = True
                        self.stack.append(p_right)
                        self.block.append(p_right)
                if p_up.color == color:
                    if not p_up.isUsed:
                        p_up.isUsed = True
                        self.stack.append(p_up)
                        self.block.append(p_up)
                if p_left.color == color:
                    if not p_left.isUsed:
                        p_left.isUsed = True
                        self.stack.append(p_left)
                        self.block.append(p_left)
            elif 0 < point.y < len(self.points[0]) - 1 and point.x == len(self.points) - 1:
                p_down = self.points[point.x][point.y + 1]
                p_up = self.points[point.x][point.y - 1]
                p_left = self.points[point.x - 1][point.y]
                if p_down.color == color:
                    if not p_down.isUsed:
                        p_down.isUsed = True
                        self.stack.append(p_down)
                        self.block.append(p_down)
                if p_up.color == color:
                    if not p_up.isUsed:
                        p_up.isUsed = True
                        self.stack.append(p_up)
                        self.block.append(p_up)
                if p_left.color == color:
                    if not p_left.isUsed:
                        p_left.isUsed = True
                        self.stack.append(p_left)
                        self.block.append(p_left)
            elif point.y == len(self.points[0]) - 1 and point.x == len(self.points) - 1:
                p_up = self.points[point.x][point.y - 1]
                p_left = self.points[point.x - 1][point.y]
                if p_up.color == color:
                    if not p_up.isUsed:
                        p_up.isUsed = True
                        self.stack.append(p_up)
                        self.block.append(p_up)
                if p_left.color == color:
                    if not p_left.isUsed:
                        p_left.isUsed = True
                        self.stack.append(p_left)
                        self.block.append(p_left)
            else:
                p_up = self.points[point.x][point.y - 1]
                p_left = self.points[point.x - 1][point.y]
                p_right = self.points[point.x + 1][point.y]
                p_down = self.points[point.x][point.y + 1]
                if p_up.color == color:
                    if not p_up.isUsed:
                        p_up.isUsed = True
                        self.stack.append(p_up)
                        self.block.append(p_up)
                if p_left.color == color:
                    if not p_left.isUsed:
                        p_left.isUsed = True
                        self.stack.append(p_left)
                        self.block.append(p_left)
                if p_right.color == color:
                    if not p_right.isUsed:
                        p_right.isUsed = True
                        self.stack.append(p_right)
                        self.block.append(p_right)
                if p_down.color == color:
                    if not p_down.isUsed:
                        p_down.isUsed = True
                        self.stack.append(p_down)
                        self.block.append(p_down)
        self.previos = len(self.block)

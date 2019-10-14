from math import inf
import operator
import sys


from .CodelChooser import CodelChooser
from .Direction import Direction, DIRECTION_POINT
from .DirectionPointer import DirectionPointer
from .Point import Point
from .ColorTable import get_command
from .Stack import Stack
from .ColorTable import COLORS
from .Color import Color

DIR_POINTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Interpreter:
    def __init__(self, image, codel_size, mode):
        self.direction_pointer = DirectionPointer()
        self.codel_chooser = CodelChooser()
        self.previous_value = None
        self.previous_color = None
        self.stack = Stack()
        self.block = []
        self.mode = mode
        self.x = 0
        self.y = 0
        self.image_map = []
        self.out = ""
        self.start_white = []
        good_codel_size = self.init_image_map_auto(image)
        if codel_size == 0:
            self.init_image_map(image, good_codel_size.pop())
        elif codel_size in good_codel_size:
            self.init_image_map(image, codel_size)
        else:
            print("Неккоректный размер кодела")
            exit(-1)
        self.find_start_point(self.image_map)
        self.command = None

    def start(self):
        self.initialize_block()
        next_pixel = self.check_end_program()
        if next_pixel is None:
            return False
        next_pixel = self.go_white(next_pixel)
        if next_pixel is None:
            return False
        self.x = next_pixel.x
        self.y = next_pixel.y

        if not self.start_white:
            self.command = get_command(self.previous_color,
                                       next_pixel.color)
            self.command(self)
        return True

    def go_white(self, next_pixel):
        self.start_white = []
        if next_pixel.color == Color.white:
            while next_pixel.color == Color.white:
                for direction in DIRECTION_POINT.keys():
                    if self.direction_pointer.direction == direction:
                        new_x = next_pixel.x + DIRECTION_POINT[direction].x
                        new_y = next_pixel.y + DIRECTION_POINT[direction].y
                        if self.image_map[new_x][new_y].color == Color.black:
                            self.direction_pointer.pointer(1)
                            self.codel_chooser.switch(1)
                            break
                        else:
                            self.start_white.append(next_pixel)
                            next_pixel = self.image_map[new_x][new_y]

                if next_pixel in self.start_white:
                    return None
        return next_pixel

    def check_end_program(self):
        k = 0
        next_pixel = None
        while k != 8:
            next_pixel = self.init_next_pixel()
            if next_pixel.color == Color.black:
                k += 1
                self.codel_chooser.switch(1)
                next_pixel = self.init_next_pixel()
                if next_pixel.color == Color.black:
                    self.direction_pointer.pointer(1)
                    k += 1
                else:
                    break
            else:
                break
        if k == 8:
            return None
        return next_pixel

    def init_image_map_auto(self, rgb_im):
        k = 1
        result = []
        while k <= min(rgb_im.height, rgb_im.width):
            flag = False
            if rgb_im.width % k == 0 and rgb_im.height % k == 0:
                for x in range(rgb_im.width):
                    for y in range(rgb_im.height):
                        if x % k == 0 and y % k == 0:
                            color = self.get_rgb(rgb_im, x, y)
                            flag = self.check_codel(k, rgb_im, x, y, color)

                if not flag:
                    result.append(k)

            k += 1
        return result

    def check_codel(self, k, rgb_im, x, y, color):
        for i in range(k):
            for j in range(k):
                color1 = self.get_rgb(rgb_im, x + i, y + j)
                if color != color1:
                    return True
        return False

    def init_image_map(self, rgb_im, codel_size):
        self.image_map = []
        if rgb_im.width % codel_size != 0 or rgb_im.height % codel_size != 0:
            print("Неверный размер кодела. Попробуйте другой.")
            sys.exit(-1)
        w = rgb_im.width // codel_size
        h = rgb_im.height // codel_size
        for x in range(w + 2):
            self.image_map.append([])
        for x in range(w + 2):
            for y in range(h + 2):
                if x == 0 or y == 0 or x == w + 1 \
                        or y == h + 1:
                    self.image_map[x].append(
                        Point(x, y, Color.black))
                else:
                    rgb = self.get_rgb(rgb_im,
                                       (x - 1) * codel_size,
                                       (y - 1) * codel_size)
                    if not (rgb in COLORS.keys()):
                        if self.mode == 0:
                            print("Неккоректный пиксель: ({}, {})"
                                  .format(x, y))
                            exit(-1)
                        if self.mode == 1:
                            self.image_map[x].append(
                                Point(x, y, Color.white))
                        if self.mode == 2:
                            self.image_map[x].append(
                                Point(x, y, Color.black))

                    else:
                        self.image_map[x].append(
                            Point(x, y, COLORS[rgb]))

    @staticmethod
    def get_rgb(rgb_im, x, y):
        r, g, b = rgb_im.getpixel((x, y))
        res = []
        rgb = [r, g, b]
        for e in rgb:
            if len(hex(e)) == 3:
                res.append(hex(e)[:2] + "0" + hex(e)[2])
            else:
                res.append(hex(e))
        return "0x" + (res[0][2:] + res[1][2:] + res[2][2:]).upper()

    def find_start_point(self, image_map):
        for y in range(len(image_map)):
            for x in range(len(image_map[0])):
                if not (self.image_map[x][y].color in
                        [Color.black, Color.white]):
                    self.x = x
                    self.y = y
                    return None

    def initialize_block(self):
        stack = []
        self.previous_color = self.image_map[self.x][self.y].color
        self.block = []
        stack.append(self.image_map[self.x][self.y])
        self.image_map[self.x][self.y].is_used = True
        self.block.append(self.image_map[self.x][self.y])
        while stack:
            point = stack.pop()
            for dp in DIR_POINTS:
                p = self.image_map[point.x + dp[0]][point.y + dp[1]]
                if p.color == self.previous_color:
                    if not p.is_used:
                        p.is_used = True
                        stack.append(p)
                        self.block.append(p)

        self.previous_value = len(self.block)
        for e in self.block:
            e.is_used = False

    def find_next_point(self, best, a1, a2, best_p, f, f2):
        for p in self.block:
            if f(getattr(p, a1), best):
                best = getattr(p, a1)
        if self.codel_chooser.direction == Direction.LEFT:
            best_p = best_p
            for p in self.block:
                if getattr(p, a1) == best:
                    if f2(getattr(p, a2), getattr(best_p, a2)):
                        best_p = p
        if self.codel_chooser.direction == Direction.RIGHT:
            best_p = -1 * best_p
            for p in self.block:
                if getattr(p, a1) == best:
                    if not f2(getattr(p, a2), getattr(best_p, a2)):
                        best_p = p
        return best_p

    def init_next_pixel(self):
        best_p = None
        if self.direction_pointer.direction == Direction.RIGHT:
            best_p = self.find_next_point(-inf, 'x', 'y',
                                          Point(inf, inf, None),
                                          operator.gt,  operator.lt)
        if self.direction_pointer.direction == Direction.DOWN:
            best_p = self.find_next_point(-inf, 'y', 'x',
                                          Point(-inf, -inf, None),
                                          operator.gt,  operator.gt)
        if self.direction_pointer.direction == Direction.LEFT:
            best_p = self.find_next_point(inf, 'x', 'y',
                                          Point(-inf, -inf, None),
                                          operator.lt, operator.gt)
        if self.direction_pointer.direction == Direction.UP:
            best_p = self.find_next_point(inf, 'y', 'x',
                                          Point(inf, inf, None),
                                          operator.lt, operator.lt)
        for direction in DIRECTION_POINT.keys():
            if self.direction_pointer.direction == direction:
                new_x = best_p.x + DIRECTION_POINT[direction].x
                new_y = best_p.y + DIRECTION_POINT[direction].y
                return self.image_map[new_x][new_y]

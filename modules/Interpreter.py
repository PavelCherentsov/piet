from math import inf
import sys
import math
from PIL import Image

from .CodelChooser import CodelChooser
from .Direction import Direction
from .DirectionPointer import DirectionPointer
from .Point import Point
from .ColorTable import get_command
from .Stack import Stack
from .ColorTable import ColorDict

DIR_POINTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Interpreter:
    def __init__(self, image, codel_size):
        self.direction_pointer = DirectionPointer()
        self.codel_chooser = CodelChooser()
        self.previous_value = None
        self.previous_color = None
        self.stack = Stack()
        self.block = []
        self.image_map = []
        self.out = ""
        self.start_white = []
        self.init_image_map(image, codel_size)
        self.init_image_map_auto(image)
        self.find_start_point(self.image_map)
        self.command = None
        self.l = len(self.image_map)

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
        if next_pixel.color == 'white':
            while next_pixel.color == 'white':
                if self.direction_pointer.direction == Direction.RIGHT:
                    if self.image_map[next_pixel.x + 1][next_pixel.y] .color \
                            == 'black':
                        self.direction_pointer.pointer(1)
                        self.codel_chooser.switch(1)
                    else:
                        self.start_white.append(next_pixel)
                        next_pixel \
                            = self.image_map[next_pixel.x + 1][next_pixel.y]
                elif self.direction_pointer.direction == Direction.DOWN:
                    if self.image_map[next_pixel.x][next_pixel.y + 1].color \
                            == 'black':
                        self.direction_pointer.pointer(1)
                        self.codel_chooser.switch(1)
                    else:
                        self.start_white.append(next_pixel)
                        next_pixel \
                            = self.image_map[next_pixel.x][next_pixel.y + 1]
                elif self.direction_pointer.direction == Direction.LEFT:
                    if self.image_map[next_pixel.x - 1][next_pixel.y].color \
                            == 'black':
                        self.direction_pointer.pointer(1)
                        self.codel_chooser.switch(1)
                    else:
                        self.start_white.append(next_pixel)
                        next_pixel \
                            = self.image_map[next_pixel.x - 1][next_pixel.y]
                elif self.direction_pointer.direction == Direction.UP:
                    if self.image_map[next_pixel.x][next_pixel.y - 1].color \
                            == 'black':
                        self.direction_pointer.pointer(1)
                        self.codel_chooser.switch(1)
                    else:
                        self.start_white.append(next_pixel)
                        next_pixel \
                            = self.image_map[next_pixel.x][next_pixel.y - 1]
                if next_pixel in self.start_white:
                    return None
        return next_pixel

    def check_end_program(self):
        k = 0

        while k != 8:
            next_pixel = self.init_next_pixel()
            print(next_pixel)
            if next_pixel.color == 'black':
                k += 1
                self.codel_chooser.switch(1)
                next_pixel = self.init_next_pixel()
                print(next_pixel)
                if next_pixel.color == 'black':
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
        flag = False
        while True:
            if rgb_im.width % k == 0 and rgb_im.height % k == 0:
                for x in range(rgb_im.width):
                    for y in range(rgb_im.height):
                        if x % k == 0 and y % k == 0:
                            r, g, b = rgb_im.getpixel((x, y))
                            r = hex(r)
                            g = hex(g)
                            b = hex(b)
                            if len(r) == 3:
                                r = r[:2] + "0" + r[2]
                            if len(g) == 3:
                                g = g[:2] + "0" + g[2]
                            if len(b) == 3:
                                b = b[:2] + "0" + b[2]
                            color = "0x" + (r[2:] + g[2:] + b[2:]).upper()
                            for i in range(k):
                                for j in range(k):
                                    r, g, b = rgb_im.getpixel((x+i, y+j))
                                    r = hex(r)
                                    g = hex(g)
                                    b = hex(b)
                                    if len(r) == 3:
                                        r = r[:2] + "0" + r[2]
                                    if len(g) == 3:
                                        g = g[:2] + "0" + g[2]
                                    if len(b) == 3:
                                        b = b[:2] + "0" + b[2]
                                    color1 = "0x" + (r[2:] + g[2:] + b[2:]).upper()
                                    if color != color1:
                                        flag = True
                            result = k
            if flag:
                break
            k += 1
        print(math.sqrt(k))


    def init_image_map(self, rgb_im, codel_size):
        if rgb_im.width % codel_size != 0 or rgb_im.height % codel_size != 0:
            print("Неерный размер кодела. Попробуйте другой.")
            sys.exit(-1)
        w = rgb_im.width // codel_size
        h = rgb_im.height // codel_size
        for x in range(w + 2):
            self.image_map.append([])
        for x in range(w + 2):
            for y in range(h + 2):
                if x == 0 or y == 0 or x == w + 1 \
                        or y == h + 1:
                    self.image_map[x].append(Point(x,
                                                   y,
                                                   ColorDict['0x000000']))
                else:
                    r, g, b = rgb_im.getpixel(((x - 1) * codel_size,
                                               (y - 1) * codel_size))
                    r = hex(r)
                    g = hex(g)
                    b = hex(b)
                    if len(r) == 3:
                        r = r[:2] + "0" + r[2]
                    if len(g) == 3:
                        g = g[:2] + "0" + g[2]
                    if len(b) == 3:
                        b = b[:2] + "0" + b[2]
                    rgb = "0x" + (r[2:] + g[2:] + b[2:]).upper()
                    self.image_map[x].append(
                        Point(x//codel_size+1, y//codel_size+1, ColorDict[rgb]))

    def find_start_point(self, image_map):
        for y in range(len(image_map)):
            for x in range(len(image_map[0])):
                if not (self.image_map[x][y].color in ['black', 'white']):
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

    @staticmethod
    def gr(x, y):
        return x > y

    @staticmethod
    def less(x, y):
        return x < y

    def find_next_point(self, best, is_x, best_p, f, f2):
        if is_x:
            for p in self.block:
                if f(p.x, best):
                    best = p.x
            if self.codel_chooser.direction == Direction.LEFT:
                best_p = best_p
                for p in self.block:
                    if p.x == best:
                        if f2(p.y, best_p.y):
                            best_p = p
            if self.codel_chooser.direction == Direction.RIGHT:
                best_p = -1 * best_p
                for p in self.block:
                    if p.x == best:
                        if not f2(p.y, best_p.y):
                            best_p = p
        else:
            for p in self.block:
                if f(p.y, best):
                    best = p.y
            if self.codel_chooser.direction == Direction.LEFT:
                best_p = best_p
                for p in self.block:
                    if p.y == best:
                        if f2(p.x, best_p.x):
                            best_p = p
            if self.codel_chooser.direction == Direction.RIGHT:
                best_p = -1*best_p
                for p in self.block:
                    if p.y == best:
                        if not f2(p.x, best_p.x):
                            best_p = p
        return best_p

    def init_next_pixel(self):

        if self.direction_pointer.direction == Direction.RIGHT:
            best_p = self.find_next_point(-inf, True, Point(inf, inf, None),
                                          self.gr, self.less)
        if self.direction_pointer.direction == Direction.DOWN:
            best_p = self.find_next_point(-inf, False, Point(-inf, -inf, None),
                                          self.gr, self.gr)
        if self.direction_pointer.direction == Direction.LEFT:
            best_p = self.find_next_point(inf, True, Point(-inf, -inf, None),
                                          self.less, self.gr)
        if self.direction_pointer.direction == Direction.UP:
            best_p = self.find_next_point(inf, False, Point(inf, inf, None),
                                          self.less, self.less)
        print("bp")
        print(best_p)
        if self.direction_pointer.direction == Direction.RIGHT:
            return self.image_map[best_p.x + 1][best_p.y]
        if self.direction_pointer.direction == Direction.DOWN:
            return self.image_map[best_p.x][best_p.y + 1]
        if self.direction_pointer.direction == Direction.LEFT:
            return self.image_map[best_p.x - 1][best_p.y]
        if self.direction_pointer.direction == Direction.UP:
            return self.image_map[best_p.x][best_p.y - 1]

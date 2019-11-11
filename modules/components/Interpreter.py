from math import inf, sqrt
import operator
from PIL import Image
from .Direction import (Direction, DIRECTION_POINT, Point,
                        CodelChooser, DirectionPointer)
from .ColorTable import COLORS, Color, COLOR_TABLE

DIR_POINTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def load_image(image):
    return Image.open(image).convert('RGB')


def get_rgb(rgb_im, x, y):
    r, g, b = rgb_im.getpixel((x, y))
    return '0x' + ('%02x%02x%02x' % (r, g, b)).upper()


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def divisor_generator(n):
    large_divisors = []
    for i in range(1, int(sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i * i != n:
                large_divisors.append(n / i)
    for divisor in reversed(large_divisors):
        yield int(divisor)


class Interpreter:
    def __init__(self, image_path, codel_size, mode):
        self.image_path = image_path
        self.image = load_image(image_path)
        self.codel_size = codel_size
        self.dir_pointer = DirectionPointer()
        self.codel_chooser = CodelChooser()
        self.previous_value = None
        self.previous_color = None
        self.stack = []
        self.block = []
        self.mode = mode
        self.x = 0
        self.y = 0
        self.stop = False
        self.image_map = []
        self.out = ""
        self.start_white = []
        self.is_in_num = False
        self.is_in_char = False
        self.is_run = True
        good_codel_size = self.init_image_map_auto(self.image)
        if codel_size == 0:
            self.init_image_map(self.image, good_codel_size.pop())
        elif codel_size in good_codel_size:
            self.init_image_map(self.image, codel_size)
        else:
            raise ValueError("Invalid codel size")
        self.find_start_point(self.image_map)
        self.command = None

    def start(self):
        self.initialize_block()
        if self.stop:
            return
        next_pixel = self.check_end_program()
        if next_pixel is None:
            self.is_run = False
            return
        next_pixel = self.go_white(next_pixel)
        if next_pixel is None:
            self.is_run = False
            return

        self.x = next_pixel.x
        self.y = next_pixel.y

        if not self.start_white:
            self.command = get_command(self.previous_color,
                                       next_pixel.color)
            try:
                return self.command(self)
            except IndexError:
                raise IndexError(
                    "Что-то не так в коделе: ({},{})".format(self.x, self.y))
        else:
            self.command = None

    def go_white(self, next_pixel):
        self.start_white = []
        if next_pixel.color == Color.white:
            while next_pixel.color == Color.white:
                for direction in DIRECTION_POINT.keys():
                    if self.dir_pointer.direction == direction:
                        new_x = next_pixel.x + DIRECTION_POINT[direction].x
                        new_y = next_pixel.y + DIRECTION_POINT[direction].y
                        if self.image_map[new_x][new_y].color == Color.black:
                            self.dir_pointer.pointer(1)
                            self.codel_chooser.switch(1)
                            break
                        else:
                            self.start_white.append(next_pixel)
                            next_pixel = self.image_map[new_x][new_y]

                if next_pixel in self.start_white:
                    return None
        return next_pixel

    def check_end_program(self):
        next_pixels = []
        start_dp_direction = self.dir_pointer.direction
        start_cc_direction = self.codel_chooser.direction
        while True:
            next_pixels.append((self.init_next_pixel(),
                                self.dir_pointer.direction,
                                self.codel_chooser.direction))
            self.codel_chooser.switch(1)
            next_pixels.append((self.init_next_pixel(),
                                self.dir_pointer.direction,
                                self.codel_chooser.direction))
            self.dir_pointer.pointer(1)
            if (self.dir_pointer.direction, self.codel_chooser.direction) == \
                    (start_dp_direction, start_cc_direction):
                break
        for e in next_pixels:
            if e[0].color != Color.black:
                self.dir_pointer.direction = e[1]
                self.codel_chooser.direction = e[2]
                return e[0]

    def init_image_map_auto(self, rgb_im):
        result = []
        for e in divisor_generator(gcd(rgb_im.height, rgb_im.width)):
            flag = False
            for x in range(rgb_im.width):
                for y in range(rgb_im.height):
                    if x % e == 0 and y % e == 0:
                        color = get_rgb(rgb_im, x, y)
                        flag = self.check_codel(e, rgb_im, x, y, color)
            if not flag:
                result.append(e)
        return result

    @staticmethod
    def check_codel(k, rgb_im, x, y, color):
        for i in range(k):
            for j in range(k):
                color1 = get_rgb(rgb_im, x + i, y + j)
                if color != color1:
                    return True
        return False

    def init_image_map(self, rgb_im, codel_size):
        self.image_map = []
        if rgb_im.width % codel_size != 0 or rgb_im.height % codel_size != 0:
            raise ValueError("Invalid codel size")
        w = rgb_im.width // codel_size
        h = rgb_im.height // codel_size
        for x in range(w + 2):
            self.image_map.append([])
        for x in range(w + 2):
            for y in range(h + 2):
                if (x in (0, w + 1)) or (y in (0, h + 1)):
                    self.image_map[x].append(
                        Point(x, y, Color.black))
                else:
                    rgb = get_rgb(rgb_im,
                                  (x - 1) * codel_size,
                                  (y - 1) * codel_size)
                    if not (rgb in COLORS.keys()):
                        if self.mode == 'None':
                            raise ValueError(
                                'Invalid Pixel: ({}, {})'.format(x, y))
                        if self.mode == 'white':
                            self.image_map[x].append(
                                Point(x, y, Color.white))
                        if self.mode == 'black':
                            self.image_map[x].append(
                                Point(x, y, Color.black))

                    else:
                        self.image_map[x].append(
                            Point(x, y, COLORS[rgb]))

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
            if e.is_stop:
                self.stop = True
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
        if self.dir_pointer.direction == Direction.RIGHT:
            best_p = self.find_next_point(-inf, 'x', 'y',
                                          Point(inf, inf, None),
                                          operator.gt, operator.lt)
        if self.dir_pointer.direction == Direction.DOWN:
            best_p = self.find_next_point(-inf, 'y', 'x',
                                          Point(-inf, -inf, None),
                                          operator.gt, operator.gt)
        if self.dir_pointer.direction == Direction.LEFT:
            best_p = self.find_next_point(inf, 'x', 'y',
                                          Point(-inf, -inf, None),
                                          operator.lt, operator.gt)
        if self.dir_pointer.direction == Direction.UP:
            best_p = self.find_next_point(inf, 'y', 'x',
                                          Point(inf, inf, None),
                                          operator.lt, operator.lt)
        for direction in DIRECTION_POINT.keys():
            if self.dir_pointer.direction == direction:
                new_x = best_p.x + DIRECTION_POINT[direction].x
                new_y = best_p.y + DIRECTION_POINT[direction].y
                return self.image_map[new_x][new_y]


class Function:
    def _push(self):
        self.stack.append(str(self.previous_value))

    def _pop(self):
        return self.stack.pop()

    def _add(self):
        self.stack.append(
            str(int(Function._pop(self)) + int(Function._pop(self))))

    def _subtract(self):
        x = Function._pop(self)
        y = Function._pop(self)
        self.stack.append(str(int(y) - int(x)))

    def _multiply(self):
        self.stack.append(
            str(int(Function._pop(self)) * int(Function._pop(self))))

    def _divide(self):
        x = Function._pop(self)
        y = Function._pop(self)
        self.stack.append(str(int(y) // int(x)))

    def _mod(self):
        x = int(Function._pop(self))
        y = int(Function._pop(self))
        while y <= 0:
            y += x
        self.stack.append(str(y % x))

    def _not(self):
        value = int(int(Function._pop(self)) == 0)
        self.stack.append(str(value))

    def _greater(self):
        x = int(Function._pop(self))
        y = int(Function._pop(self))
        if y > x:
            self.stack.append('1')
        else:
            self.stack.append('0')

    def _duplicate(self):
        e = Function._pop(self)
        self.stack.append(e)
        self.stack.append(e)

    def _out_num(self):
        e = Function._pop(self)
        self.out += str(e)
        return e

    def _out_char(self):
        e = chr(int(Function._pop(self)))
        self.out += e
        return e

    def _in_num(self):
        self.is_in_num = True

    def _in_char(self):
        self.is_in_char = True

    def _switch(self):
        self.codel_chooser.switch(int(Function._pop(self)))

    def _pointer(self):
        self.dir_pointer.pointer(int(Function._pop(self)))

    def _roll(self):
        num = int(Function._pop(self))
        depth = int(Function._pop(self))
        num %= depth
        x = -abs(num) + depth * (num < 0)
        self.stack[-depth:] = \
            self.stack[x:] + self.stack[-depth:x]

    FUNCTION_TABLE = [[None, _push, _pop],
                      [_add, _subtract, _multiply],
                      [_divide, _mod, _not],
                      [_greater, _pointer, _switch],
                      [_duplicate, _roll, _in_num],
                      [_in_char, _out_num, _out_char]]


def get_command(c1, c2):
    (c1_x, c1_y) = (0, 0)
    (c2_x, c2_y) = (0, 0)
    for i in range(3):
        for j in range(6):
            if COLOR_TABLE[i][j] == c1:
                (c1_x, c1_y) = (j, i)
            if COLOR_TABLE[i][j] == c2:
                (c2_x, c2_y) = (j, i)
    if c2_x - c1_x < 0:
        c2_x += 6
    if c2_y - c1_y < 0:
        c2_y += 3
    return Function.FUNCTION_TABLE[c2_x - c1_x][c2_y - c1_y]

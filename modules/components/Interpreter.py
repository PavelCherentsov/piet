from math import inf, sqrt
import operator
from enum import Enum
from .Direction import (Direction, DIRECTION_POINT, Point,
                        CodelChooser, DirectionPointer)
from .ColorTable import Color, COLOR_TABLE

DIR_POINTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


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


class State(Enum):
    STOPPED = 0,
    RUNNING = 1,
    WAIT_INPUT = 2,
    END = 3,


class Interpreter:
    def __init__(self, image_path, image_map, codel_size, mode):
        self.image_path = image_path
        self.image_map = image_map
        self.codel_size = codel_size
        self.mode = mode
        self.image_map_start = image_map
        self.dir_pointer = DirectionPointer()
        self.codel_chooser = CodelChooser()

        self.previous_value = None
        self.previous_color = None
        self.stack = []
        self.block = []
        self.x = 0
        self.y = 0

        self.output = None
        self.input = None

        self.start_white = []

        self.state = State.RUNNING

        self.is_in_num = False
        self.is_in_char = False

        self.goods_codel_sizes = self.get_goods_codel_sizes()
        if codel_size == 0:
            self.init_image_map(self.goods_codel_sizes.pop())
        elif codel_size in self.goods_codel_sizes:
            self.init_image_map(self.codel_size)
        else:
            raise ValueError("Invalid codel size")
        self.find_start_point(self.image_map)
        self.command = None
        self.next_command = None
        self.set_next_command(self.image_map[self.x][self.y])

    def step(self):
        self.initialize_block()

        if self.state == State.STOPPED:
            return

        next_pixel = self.check_end_program()
        if next_pixel is None:
            self.state = State.END
            return
        next_pixel = self.go_white(next_pixel)
        if next_pixel is None:
            self.state = State.END
            return

        self.x = next_pixel.x
        self.y = next_pixel.y

        res = None

        if not self.start_white:
            self.command = get_command(self.previous_color,
                                       next_pixel.color)
            try:
                res = self.command(self)
            except IndexError as e:
                raise IndexError(
                    "\nInvalid command in the codel: ({},{})"
                    .format(self.x, self.y)) from e
        else:
            self.command = None

        if res is not None:
            self.output(res)

        if self.state == State.WAIT_INPUT:
            self.input_start()
        if next_pixel is not None:
            self.set_next_command(next_pixel)

    def input_start(self):
        if self.is_in_num:
            try:
                self.stack.append(str(int(self.input())))
            except ValueError as e:
                raise ValueError("Enter the number") from e
            self.is_in_num = False
        if self.is_in_char:
            try:
                self.stack.append(str(ord(self.input())))
            except ValueError as e:
                raise ValueError("Enter one character") from e
            self.is_in_char = False
        self.state = State.RUNNING

    def set_next_command(self, current_pixel):
        self.initialize_block()
        next_pixel = self.check_end_program()
        if next_pixel is None:
            return
        next_pixel = self.go_white(next_pixel)
        if next_pixel is None:
            return
        self.next_command = get_command(current_pixel.color, next_pixel.color)

    def go_white(self, next_pixel):
        self.start_white = []
        if next_pixel.color == Color.WHITE:
            while next_pixel.color == Color.WHITE:
                for direction in DIRECTION_POINT.keys():
                    if self.dir_pointer.direction == direction:
                        new_x = next_pixel.x + DIRECTION_POINT[direction].x
                        new_y = next_pixel.y + DIRECTION_POINT[direction].y
                        if self.image_map[new_x][new_y].color == Color.BLACK:
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
            if e[0].color != Color.BLACK:
                self.dir_pointer.direction = e[1]
                self.codel_chooser.direction = e[2]
                return e[0]

    def get_goods_codel_sizes(self):
        result = []
        for e in divisor_generator(
                gcd(len(self.image_map), len(self.image_map[0]))):
            flag = False
            for x in range(len(self.image_map)):
                for y in range(len(self.image_map[0])):
                    if x % e == 0 and y % e == 0:
                        color = self.image_map[x][y]
                        flag = self.check_codel(e, x, y, color, flag)
            if not flag:
                result.append(e)
        return result

    def check_codel(self, k, x, y, color, flag):
        for i in range(k):
            for j in range(k):
                color1 = self.image_map[x + i][y + j]
                if color != color1:
                    return True
        if flag:
            return True
        return False

    def init_image_map(self, codel_size):
        if len(self.image_map[0]) % codel_size != 0 or \
                len(self.image_map) % codel_size != 0:
            raise ValueError("Invalid codel size")
        image_map = []
        w = (len(self.image_map)) // codel_size
        h = (len(self.image_map[0])) // codel_size
        for x in range(w + 2):
            image_map.append([])
        for x in range(w + 2):
            for y in range(h + 2):
                if (x in (0, w + 1)) or (y in (0, h + 1)):
                    image_map[x].append(Point(x, y, Color.BLACK))
                else:
                    color = self.image_map[(x - 1) * codel_size][
                        (y - 1) * codel_size]
                    if not (Color.WHITE.value <= color <= Color.BLACK.value):
                        if self.mode == 'None':
                            x = x * codel_size
                            y = y * codel_size
                            color = self.image_map[x - 1][y - 1]
                            raise ValueError(
                                f'Invalid Pixel: ({x}, {y}), color: {color}')
                        if self.mode == 'white':
                            image_map[x].append(Point(x, y, Color.WHITE))
                        if self.mode == 'black':
                            image_map[x].append(Point(x, y, Color.BLACK))
                    else:
                        image_map[x].append(Point(x, y, Color(color)))

        self.image_map = image_map

    def find_start_point(self, image_map):
        for y in range(len(image_map[0])):
            for x in range(len(image_map)):
                if not (self.image_map[x][y].color in
                        [Color.BLACK, Color.WHITE]):
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
                self.state = State.STOPPED
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


def command(name):
    def decorator(func):
        func.name = name
        return func

    return decorator


class Function:
    @command('push')
    def _push(self):
        self.stack.append(str(self.previous_value))

    @command('pop')
    def _pop(self):
        return self.stack.pop()

    @command('add')
    def _add(self):
        self.stack.append(
            str(int(Function._pop(self)) + int(Function._pop(self))))

    @command('subtract')
    def _subtract(self):
        x = Function._pop(self)
        y = Function._pop(self)
        self.stack.append(str(int(y) - int(x)))

    @command('multiply')
    def _multiply(self):
        self.stack.append(
            str(int(Function._pop(self)) * int(Function._pop(self))))

    @command('divide')
    def _divide(self):
        x = Function._pop(self)
        y = Function._pop(self)
        self.stack.append(str(int(y) // int(x)))

    @command('mod')
    def _mod(self):
        x = int(Function._pop(self))
        y = int(Function._pop(self))
        while y <= 0:
            y += x
        self.stack.append(str(y % x))

    @command('not')
    def _not(self):
        value = int(int(Function._pop(self)) == 0)
        self.stack.append(str(value))

    @command('greater')
    def _greater(self):
        x = int(Function._pop(self))
        y = int(Function._pop(self))
        if y > x:
            self.stack.append('1')
        else:
            self.stack.append('0')

    @command('duplicate')
    def _duplicate(self):
        e = Function._pop(self)
        self.stack.append(e)
        self.stack.append(e)

    @command('output num')
    def _out_num(self):
        return Function._pop(self)

    @command('output char')
    def _out_char(self):
        return chr(int(Function._pop(self)))

    @command('input num')
    def _in_num(self):
        self.state = State.WAIT_INPUT
        self.is_in_num = True

    @command('input char')
    def _in_char(self):
        self.state = State.WAIT_INPUT
        self.is_in_char = True

    @command('switch')
    def _switch(self):
        self.codel_chooser.switch(int(Function._pop(self)))

    @command('pointer')
    def _pointer(self):
        self.dir_pointer.pointer(int(Function._pop(self)))

    @command('roll')
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

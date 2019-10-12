import os
import sys
import unittest

from PIL import Image

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from modules.Point import Point
from modules.Interpreter import Interpreter
from modules.Direction import Direction
from modules.Stack import Stack
import modules.Function
from modules.ColorTable import get_command


class GameTest(unittest.TestCase):

    def test_init_image_map(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1)
        i.init_image_map(image, 1)
        self.assertEqual(i.image_map[0][0].color, 'black')
        self.assertNotEqual(i.image_map[1][1].color, 'black')

    def test_init_next_pixel(self):
        image = Image.open("tests/programs/HelloWorld.png").convert('RGB')
        i = Interpreter(image, 1)
        i.init_image_map(image, 1)
        i.find_start_point(i.image_map)
        i.initialize_block()
        p = i.init_next_pixel()
        self.assertEqual(p.x, 6)
        self.assertEqual(p.y, 1)

    def test_end_program(self):
        image = Image.open("tests/programs/HelloWorld.png").convert('RGB')
        i = Interpreter(image, 1)
        i.init_image_map(image, 1)
        i.find_start_point(i.image_map)
        i.initialize_block()
        p = i.init_next_pixel()
        p = i.check_end_program()
        #self.assertEqual(p, None)

    def test_white(self):
        image = Image.open("tests/programs/white.png").convert('RGB')
        i = Interpreter(image, 1)
        i.init_image_map(image, 1)
        i.x = 1
        i.y = 1
        i.initialize_block()
        p = i.go_white(Point(1, 1, 'white'))
        self.assertEqual(p, None)

    def test_dp_pointer(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1)
        self.assertEqual(i.direction_pointer.direction, Direction(0))
        i.direction_pointer.pointer(1)
        self.assertEqual(i.direction_pointer.direction, Direction(1))
        i.direction_pointer.pointer(-1)
        self.assertEqual(i.direction_pointer.direction, Direction(0))
        i.direction_pointer.pointer(4)
        self.assertEqual(i.direction_pointer.direction, Direction(0))

    def test_cc_switch(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1)
        self.assertEqual(i.codel_chooser.direction, Direction(2))
        i.codel_chooser.switch(1)
        self.assertEqual(i.codel_chooser.direction, Direction(0))
        i.codel_chooser.switch(2)
        self.assertEqual(i.codel_chooser.direction, Direction(0))
        i.codel_chooser.switch(1)
        self.assertEqual(i.codel_chooser.direction, Direction(2))

    def test_point(self):
        p = Point(10, 5, 'black')
        p = -1 * p
        self.assertEqual(p.x, -10)
        self.assertEqual(p.y, -5)

    def test_stack(self):
        s = Stack()
        st = str(s)

        s.push(1)
        st = str(s)
        self.assertEqual(s.pop(), 1)
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.pop(), 3)

    def test_get_command(self):
        self.assertEqual(get_command('red', 'yellow'),
                         modules.Function._add)
        self.assertEqual(get_command('red', 'blue'),
                         modules.Function._duplicate)
        self.assertEqual(get_command('red', 'light red'),
                         modules.Function._pop)
        self.assertEqual(get_command('red', 'dark red'),
                         modules.Function._push)
        self.assertEqual(get_command('blue', 'light red'),
                         modules.Function._not)

    def test_functions(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image,1)
        i.previous_value = 23
        modules.Function._push(i)
        self.assertEqual(i.stack.pop(), 23)
        i.previous_value = 23
        modules.Function._push(i)
        modules.Function._pop(i)
        self.assertEqual(i.stack.stack, [])
        i.previous_value = 23
        modules.Function._push(i)
        i.previous_value = 32
        modules.Function._push(i)
        modules.Function._add(i)
        self.assertEqual(i.stack.pop(), 55)
        i.previous_value = 23
        modules.Function._push(i)
        i.previous_value = 32
        modules.Function._push(i)
        modules.Function._subtract(i)
        self.assertEqual(i.stack.pop(), -9)
        i.previous_value = 7
        modules.Function._push(i)
        i.previous_value = 8
        modules.Function._push(i)
        modules.Function._multiply(i)
        self.assertEqual(i.stack.pop(), 56)
        i.previous_value = 40
        modules.Function._push(i)
        i.previous_value = 8
        modules.Function._push(i)
        modules.Function._divide(i)
        self.assertEqual(i.stack.pop(), 5)
        i.previous_value = 5
        modules.Function._push(i)
        i.previous_value = 3
        modules.Function._push(i)
        modules.Function._mod(i)
        self.assertEqual(i.stack.pop(), 2)
        i.previous_value = -2
        modules.Function._push(i)
        i.previous_value = 3
        modules.Function._push(i)
        modules.Function._mod(i)
        self.assertEqual(i.stack.pop(), 1)
        i.previous_value = 0
        modules.Function._push(i)
        modules.Function._not(i)
        self.assertEqual(i.stack.pop(), 1)
        i.previous_value = 23
        modules.Function._push(i)
        modules.Function._not(i)
        self.assertEqual(i.stack.pop(), 0)
        i.previous_value = 23
        modules.Function._push(i)
        modules.Function._not(i)
        self.assertEqual(i.stack.pop(), 0)
        i.previous_value = 1
        modules.Function._push(i)
        i.previous_value = 2
        modules.Function._push(i)
        modules.Function._greater(i)
        self.assertEqual(i.stack.pop(), 0)
        i.previous_value = 1
        modules.Function._push(i)
        i.previous_value = 0
        modules.Function._push(i)
        modules.Function._greater(i)
        self.assertEqual(i.stack.pop(), 1)
        i.previous_value = 23
        modules.Function._push(i)
        modules.Function._duplicate(i)
        self.assertEqual(i.stack.pop(), 23)
        self.assertEqual(i.stack.pop(), 23)
        i.previous_value = 111
        modules.Function._push(i)
        modules.Function._switch(i)
        self.assertEqual(i.stack.stack, [])
        self.assertEqual(i.codel_chooser.direction, Direction.RIGHT)
        i.previous_value = 110
        modules.Function._push(i)
        modules.Function._switch(i)
        self.assertEqual(i.stack.stack, [])
        self.assertEqual(i.codel_chooser.direction, Direction.RIGHT)
        i.previous_value = 111
        modules.Function._push(i)
        modules.Function._switch(i)
        self.assertEqual(i.stack.stack, [])
        self.assertEqual(i.codel_chooser.direction, Direction.LEFT)
        i.previous_value = 40
        modules.Function._push(i)
        modules.Function._pointer(i)
        self.assertEqual(i.stack.stack, [])
        self.assertEqual(i.direction_pointer.direction, Direction.RIGHT)
        i.previous_value = 41
        modules.Function._push(i)
        modules.Function._pointer(i)
        self.assertEqual(i.stack.stack, [])
        self.assertEqual(i.direction_pointer.direction, Direction.DOWN)
        i.previous_value = 41
        modules.Function._push(i)
        modules.Function._pointer(i)
        self.assertEqual(i.stack.stack, [])
        self.assertEqual(i.direction_pointer.direction, Direction.LEFT)
        i.previous_value = 42
        modules.Function._push(i)
        modules.Function._pointer(i)
        self.assertEqual(i.stack.stack, [])
        self.assertEqual(i.direction_pointer.direction, Direction.RIGHT)
        i.stack.stack = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 5, 3]
        modules.Function._roll(i)
        self.assertEqual(i.stack.stack[0], 1)
        self.assertEqual(i.stack.stack[1], 2)
        self.assertEqual(i.stack.stack[2], 3)
        self.assertEqual(i.stack.stack[3], 4)
        self.assertEqual(i.stack.stack[4], 5)
        self.assertEqual(i.stack.stack[5], 8)
        self.assertEqual(i.stack.stack[6], 9)
        self.assertEqual(i.stack.stack[7], 10)
        self.assertEqual(i.stack.stack[8], 6)
        self.assertEqual(i.stack.stack[9], 7)
        modules.Function._out_char(i)
        modules.Function._out_num(i)


if __name__ == '__main__':
    unittest.main()

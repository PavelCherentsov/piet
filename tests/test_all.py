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
from modules.Color import Color


class InterpreterTest(unittest.TestCase):

    def test_find_start_point(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        i.init_image_map(image, 1)
        i.find_start_point(i.image_map)
        self.assertEqual(i.x, 1)
        self.assertEqual(i.y, 1)

    def test_init_block(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        i.init_image_map(image, 1)
        i.find_start_point(i.image_map)
        i.initialize_block()
        self.assertEqual(i.previous_color, Color.light_red)
        self.assertEqual(i.previous_value, 16)

    def test_start(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        i.init_image_map(image, 1)
        i.find_start_point(i.image_map)
        i.start()
        self.assertEqual(i.x, 5)
        self.assertEqual(i.y, 1)

    def test_init_image_map(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        i.init_image_map(image, 1)
        self.assertEqual(i.image_map[0][0].color, Color.black)
        self.assertNotEqual(i.image_map[1][1].color, Color.black)

    def test_get_rgb(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        res = i.get_rgb(image, 0, 0)
        self.assertEqual(res, '0xFFC0C0')
        res = i.get_rgb(image, 5, 0)
        self.assertEqual(res, '0xFFFFFF')

    def test_init_image_map_auto(self):
        image = Image.open("tests/programs/HelloWorld.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        res = i.init_image_map_auto(image)
        self.assertEqual(res.pop(), 1)
        image = Image.open("tests/programs/HelloWorld5.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        res = i.init_image_map_auto(image)
        self.assertEqual(res.pop(), 5)

    def test_init_next_pixel(self):
        image = Image.open("tests/programs/HelloWorld.png").convert('RGB')
        i = Interpreter(image, 1, 2)
        i.init_image_map(image, 1)
        i.find_start_point(i.image_map)
        i.initialize_block()
        p = i.init_next_pixel()
        self.assertEqual(p.x, 6)
        self.assertEqual(p.y, 1)

    def test_end_program(self):
        image = Image.open("tests/programs/black.png").convert('RGB')
        i = Interpreter(image, 1, 1)
        i.init_image_map(image, 1)
        i.find_start_point(i.image_map)
        i.initialize_block()
        p = i.check_end_program()
        self.assertEqual(p, None)

    def test_white(self):
        image = Image.open("tests/programs/white.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        i.init_image_map(image, 1)
        i.x = 1
        i.y = 1
        i.initialize_block()
        p = i.go_white(Point(1, 1, Color.white))
        self.assertEqual(p, None)

    def test_dp_pointer(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        self.assertEqual(i.direction_pointer.direction, Direction(0))
        i.direction_pointer.pointer(1)
        self.assertEqual(i.direction_pointer.direction, Direction(1))
        i.direction_pointer.pointer(-1)
        self.assertEqual(i.direction_pointer.direction, Direction(0))
        i.direction_pointer.pointer(4)
        self.assertEqual(i.direction_pointer.direction, Direction(0))

    def test_cc_switch(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
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
        str(s)
        s.push(1)
        str(s)
        for r in range(10):
            s.push(1)
        str(s)
        self.assertEqual(s.pop(), 1)
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.pop(), 3)

    def test_get_command(self):
        self.assertEqual(get_command(Color.red, Color.yellow),
                         modules.Function._add)
        self.assertEqual(get_command(Color.red, Color.blue),
                         modules.Function._duplicate)
        self.assertEqual(get_command(Color.red, Color.light_red),
                         modules.Function._pop)
        self.assertEqual(get_command(Color.red, Color.dark_red),
                         modules.Function._push)
        self.assertEqual(get_command(Color.blue, Color.light_red),
                         modules.Function._not)

    def test_functions_push(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        i.previous_value = 23
        modules.Function._push(i)
        self.assertEqual(i.stack.pop(), 23)

    def test_functions_pop(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        i.previous_value = 23
        modules.Function._push(i)
        modules.Function._pop(i)
        self.assertEqual(i.stack.stack, [])

    def test_functions_add(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        i.previous_value = 23
        modules.Function._push(i)
        i.previous_value = 32
        modules.Function._push(i)
        modules.Function._add(i)
        self.assertEqual(i.stack.pop(), 55)

    def test_functions_sub(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        i.previous_value = 23
        modules.Function._push(i)
        i.previous_value = 32
        modules.Function._push(i)
        modules.Function._subtract(i)
        self.assertEqual(i.stack.pop(), -9)

    def test_functions_mul(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        i.previous_value = 7
        modules.Function._push(i)
        i.previous_value = 8
        modules.Function._push(i)
        modules.Function._multiply(i)
        self.assertEqual(i.stack.pop(), 56)

    def test_functions_div(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        i.previous_value = 40
        modules.Function._push(i)
        i.previous_value = 8
        modules.Function._push(i)
        modules.Function._divide(i)
        self.assertEqual(i.stack.pop(), 5)

    def test_functions_mod(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
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

    def test_functions_not(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
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

    def test_functions_gr(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
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

    def test_functions_duplicate(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        i.previous_value = 23
        modules.Function._push(i)
        modules.Function._duplicate(i)
        self.assertEqual(i.stack.pop(), 23)
        self.assertEqual(i.stack.pop(), 23)

    def test_functions_switch(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
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

    def test_functions_pointer(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
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

    def test_functions_roll_out(self):
        image = Image.open("tests/programs/push.png").convert('RGB')
        i = Interpreter(image, 1, 0)
        i.stack.stack = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 5, 3]
        modules.Function._roll(i)
        result = [1, 2, 3, 4, 5, 8, 9, 10, 6, 7]
        self.assertEqual(i.stack.stack, result)
        modules.Function._out_char(i)
        modules.Function._out_num(i)


if __name__ == '__main__':
    unittest.main()

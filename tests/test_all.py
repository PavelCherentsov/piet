import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from modules.components.Interpreter import (Interpreter, get_rgb, get_command,
                                            Function)
from modules.components.Direction import Direction, Point
from modules.components.ColorTable import Color



class InterpreterInputTest(unittest.TestCase):
    def test_find_start_point2(self):
        image = "tests/programs/HelloWorld4.png"
        i = Interpreter(image, 2, 0)
        i.init_image_map(i.image, 2)
        i.find_start_point(i.image_map)
        self.assertEqual(i.x, 3)
        self.assertEqual(i.y, 1)

    def test_find_start_point4(self):
        image = "tests/programs/HelloWorld4.png"
        i = Interpreter(image, 4, 0)
        i.init_image_map(i.image, 4)
        i.find_start_point(i.image_map)
        self.assertEqual(i.x, 2)
        self.assertEqual(i.y, 1)

    def test_find_start_point_auto(self):
        image = "tests/programs/HelloWorld4.png"
        i = Interpreter(image, 0, 0)
        self.assertEqual(i.init_image_map_auto(i.image), [1, 2, 4])


class InterpreterValidTest(unittest.TestCase):

    def test_init_block(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.init_image_map(i.image, 1)
        i.find_start_point(i.image_map)
        i.initialize_block()
        self.assertEqual(i.previous_color, Color.light_red)
        self.assertEqual(i.previous_value, 16)

    def test_start(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.init_image_map(i.image, 1)
        i.find_start_point(i.image_map)
        i.start()
        self.assertEqual(i.x, 5)
        self.assertEqual(i.y, 1)

    def test_init_image_map(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.init_image_map(i.image, 1)
        self.assertEqual(i.image_map[0][0].color, Color.black)
        self.assertNotEqual(i.image_map[1][1].color, Color.black)

    def test_get_rgb(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        res = get_rgb(i.image, 0, 0)
        self.assertEqual(res, '0xFFC0C0')
        res = get_rgb(i.image, 5, 0)
        self.assertEqual(res, '0xFFFFFF')

    def test_init_image_map_auto(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        res = i.init_image_map_auto(i.image)
        self.assertEqual(res.pop(), 5)

    def test_init_next_pixel(self):
        image = "tests/programs/HelloWorld.png"
        i = Interpreter(image, 1, 2)
        i.init_image_map(i.image, 1)
        i.find_start_point(i.image_map)
        i.initialize_block()
        p = i.init_next_pixel()
        self.assertEqual(p.x, 6)
        self.assertEqual(p.y, 1)

    def test_end_program(self):
        image = "tests/programs/black.png"
        i = Interpreter(image, 1, 1)
        i.init_image_map(i.image, 1)
        i.find_start_point(i.image_map)
        i.initialize_block()
        p = i.check_end_program()
        self.assertEqual(p, None)

    def test_white(self):
        image = "tests/programs/white.png"
        i = Interpreter(image, 1, 0)
        i.init_image_map(i.image, 1)
        i.x = 1
        i.y = 1
        i.initialize_block()
        p = i.go_white(Point(1, 1, Color.white))
        self.assertEqual(p, None)


class InterpreterTest(unittest.TestCase):
    def test_dp_pointer(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        self.assertEqual(i.dir_pointer.direction, Direction(0))
        i.dir_pointer.pointer(1)
        self.assertEqual(i.dir_pointer.direction, Direction(1))
        i.dir_pointer.pointer(-1)
        self.assertEqual(i.dir_pointer.direction, Direction(0))
        i.dir_pointer.pointer(4)
        self.assertEqual(i.dir_pointer.direction, Direction(0))

    def test_cc_switch(self):
        image = "tests/programs/push.png"
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
        stack = list()
        stack.append(1)
        for r in range(10):
            stack.append(1)
        self.assertEqual(stack.pop(), 1)
        stack.append(1)
        stack.append(2)
        stack.append(3)
        self.assertEqual(stack.pop(), 3)

    def test_get_command(self):
        self.assertEqual(get_command(Color.red, Color.yellow),
                         Function._add)
        self.assertEqual(get_command(Color.red, Color.blue),
                         Function._duplicate)
        self.assertEqual(get_command(Color.red, Color.light_red),
                         Function._pop)
        self.assertEqual(get_command(Color.red, Color.dark_red),
                         Function._push)
        self.assertEqual(get_command(Color.blue, Color.light_red),
                         Function._not)

    def test_functions_push(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.previous_value = 23
        Function._push(i)
        self.assertEqual(i.stack.pop(), '23')

    def test_functions_pop(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.previous_value = 23
        Function._push(i)
        Function._pop(i)
        self.assertEqual(i.stack, [])

    def test_functions_add(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.previous_value = 23
        Function._push(i)
        i.previous_value = 32
        Function._push(i)
        Function._add(i)
        self.assertEqual(i.stack.pop(), '55')

    def test_functions_sub(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.previous_value = 23
        Function._push(i)
        i.previous_value = 32
        Function._push(i)
        Function._subtract(i)
        self.assertEqual(i.stack.pop(), '-9')

    def test_functions_mul(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.previous_value = 7
        Function._push(i)
        i.previous_value = 8
        Function._push(i)
        Function._multiply(i)
        self.assertEqual(i.stack.pop(), '56')

    def test_functions_div(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.previous_value = 40
        Function._push(i)
        i.previous_value = 8
        Function._push(i)
        Function._divide(i)
        self.assertEqual(i.stack.pop(), '5')

    def test_functions_mod(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.previous_value = 5
        Function._push(i)
        i.previous_value = 3
        Function._push(i)
        Function._mod(i)
        self.assertEqual(i.stack.pop(), '2')
        i.previous_value = -2
        Function._push(i)
        i.previous_value = 3
        Function._push(i)
        Function._mod(i)
        self.assertEqual(i.stack.pop(), '1')

    def test_functions_not(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.previous_value = 0
        Function._push(i)
        Function._not(i)
        self.assertEqual(i.stack.pop(), '1')
        i.previous_value = 23
        Function._push(i)
        Function._not(i)
        self.assertEqual(i.stack.pop(), '0')
        i.previous_value = 23
        Function._push(i)
        Function._not(i)
        self.assertEqual(i.stack.pop(), '0')

    def test_functions_gr(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.previous_value = 1
        Function._push(i)
        i.previous_value = 2
        Function._push(i)
        Function._greater(i)
        self.assertEqual(i.stack.pop(), '0')
        i.previous_value = 1
        Function._push(i)
        i.previous_value = 0
        Function._push(i)
        Function._greater(i)
        self.assertEqual(i.stack.pop(), '1')

    def test_functions_duplicate(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.previous_value = 23
        Function._push(i)
        Function._duplicate(i)
        self.assertEqual(i.stack.pop(), '23')
        self.assertEqual(i.stack.pop(), '23')

    def test_functions_switch(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.previous_value = 111
        Function._push(i)
        Function._switch(i)
        self.assertEqual(i.stack, [])
        self.assertEqual(i.codel_chooser.direction, Direction.RIGHT)
        i.previous_value = 110
        Function._push(i)
        Function._switch(i)
        self.assertEqual(i.stack, [])
        self.assertEqual(i.codel_chooser.direction, Direction.RIGHT)
        i.previous_value = 111
        Function._push(i)
        Function._switch(i)
        self.assertEqual(i.stack, [])
        self.assertEqual(i.codel_chooser.direction, Direction.LEFT)

    def test_functions_pointer(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.previous_value = 40
        Function._push(i)
        Function._pointer(i)
        self.assertEqual(i.stack, [])
        self.assertEqual(i.dir_pointer.direction, Direction.RIGHT)
        i.previous_value = 41
        Function._push(i)
        Function._pointer(i)
        self.assertEqual(i.stack, [])
        self.assertEqual(i.dir_pointer.direction, Direction.DOWN)
        i.previous_value = 41
        Function._push(i)
        Function._pointer(i)
        self.assertEqual(i.stack, [])
        self.assertEqual(i.dir_pointer.direction, Direction.LEFT)
        i.previous_value = 42
        Function._push(i)
        Function._pointer(i)
        self.assertEqual(i.stack, [])
        self.assertEqual(i.dir_pointer.direction, Direction.RIGHT)

    def test_functions_roll_out(self):
        image = "tests/programs/push.png"
        i = Interpreter(image, 1, 0)
        i.stack = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 5, 3]
        Function._roll(i)
        result = [1, 2, 3, 4, 5, 8, 9, 10, 6, 7]
        self.assertEqual(i.stack, result)
        Function._out_char(i)
        Function._out_num(i)


if __name__ == '__main__':
    unittest.main()

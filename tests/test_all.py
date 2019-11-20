import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from modules.components.Interpreter import (Interpreter, get_command,
                                            Function, State)
from modules.components.Direction import Direction, Point
from modules.components.ColorTable import Color
from modules.ParseImage import load_image, create_image_map


class InterpreterParseImageTest(unittest.TestCase):
    def test_correct_parse(self):
        actual_image_map = create_image_map(
            load_image("tests/programs/colors.png"))
        expected_image_map = [[0, 5, 10, 15],
                              [1, 6, 11, 16],
                              [2, 7, 12, 17],
                              [3, 8, 13, 18],
                              [4, 9, 14, 19]]
        self.assertEqual(actual_image_map, expected_image_map)

    def test_wrong_color(self):
        actual_image_map = create_image_map(
            load_image("tests/programs/wrong_color.png"))
        expected_image_map = [['0xFFBAEB']]
        self.assertEqual(actual_image_map, expected_image_map)


class InterpreterInputTest(unittest.TestCase):
    def test_get_goods_codel_size(self):
        image_map = [[1, 1, 1, 1],
                     [1, 1, 1, 1],
                     [1, 1, 1, 1],
                     [1, 1, 1, 1]]
        i = Interpreter('path', image_map, 1, 'None')
        actual_good_sizes = i.goods_codel_sizes
        expected_good_sizes = [1, 2, 4]
        self.assertEqual(actual_good_sizes, expected_good_sizes)

    def test_find_start_point1(self):
        image_map = [[0, 0, 1, 1],
                     [0, 0, 1, 1],
                     [1, 1, 1, 1],
                     [1, 1, 1, 1]]
        i = Interpreter('path', image_map, 1, 'None')
        self.assertEqual(i.x, 3)
        self.assertEqual(i.y, 1)

    def test_find_start_point2(self):
        image_map = [[0, 0, 1, 1],
                     [0, 0, 1, 1],
                     [1, 1, 1, 1],
                     [1, 1, 1, 1]]
        i = Interpreter('path', image_map, 2, 'None')
        self.assertEqual(i.x, 2)
        self.assertEqual(i.y, 1)


class InterpreterValidTest(unittest.TestCase):

    def test_init_block(self):
        image_map = [[0, 0, 1, 1],
                     [0, 0, 1, 1],
                     [1, 1, 1, 1],
                     [1, 1, 1, 1]]
        i = Interpreter('path', image_map, 1, 'None')
        i.initialize_block()
        self.assertEqual(i.previous_color, Color.LIGHT_RED)
        self.assertEqual(i.previous_value, 12)

    def test_init_image_map(self):
        image_map = [[0, 0, 1, 1],
                     [0, 0, 1, 1],
                     [1, 1, 1, 1],
                     [1, 1, 1, 1]]
        i = Interpreter('path', image_map, 1, 'None')
        self.assertEqual(i.image_map[0][0].color, Color.BLACK)
        self.assertNotEqual(i.image_map[1][1].color, Color.BLACK)

    def test_init_next_pixel(self):
        image_map = [[1, 2],
                     [1, 4],
                     [2, 5]]
        i = Interpreter('path', image_map, 1, 'None')
        i.find_start_point(i.image_map)
        i.initialize_block()
        p = i.init_next_pixel()
        self.assertEqual(p.x, 3)
        self.assertEqual(p.y, 1)

    def test_end_program(self):
        image_map = [[1, 19],
                     [19, 19]]
        i = Interpreter('path', image_map, 1, 'None')
        i.find_start_point(i.image_map)
        i.initialize_block()
        p = i.check_end_program()
        self.assertEqual(p, None)

    def test_white(self):
        image_map = [[0, 0, 0],
                     [0, 1, 0],
                     [0, 0, 0]]
        i = Interpreter('path', image_map, 1, 'None')
        i.x = 1
        i.y = 1
        i.initialize_block()
        p = i.go_white(Point(1, 1, Color.WHITE))
        self.assertEqual(p, None)


class InterpreterFunctionsTest(unittest.TestCase):
    def test_dp_pointer(self):
        image_map = [[1, 2],
                     [2, 1]]
        i = Interpreter('path', image_map, 1, 'None')
        self.assertEqual(i.dir_pointer.direction, Direction(0))
        i.dir_pointer.pointer(1)
        self.assertEqual(i.dir_pointer.direction, Direction(1))
        i.dir_pointer.pointer(-1)
        self.assertEqual(i.dir_pointer.direction, Direction(0))
        i.dir_pointer.pointer(4)
        self.assertEqual(i.dir_pointer.direction, Direction(0))

    def test_dp_pointer(self):
        image_map = [[1, 2],
                     [2, 1]]
        i = Interpreter('path', image_map, 1, 'None')
        self.assertEqual(i.dir_pointer.direction, Direction(0))
        i.dir_pointer.pointer(1)
        self.assertEqual(i.dir_pointer.direction, Direction(1))
        i.dir_pointer.pointer(-1)
        self.assertEqual(i.dir_pointer.direction, Direction(0))
        i.dir_pointer.pointer(4)
        self.assertEqual(i.dir_pointer.direction, Direction(0))

    def test_cc_switch(self):
        image_map = [[1, 2],
                     [2, 1]]
        i = Interpreter('path', image_map, 1, 'None')
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
        self.assertEqual(get_command(Color.RED, Color.YELLOW),
                         Function._add)
        self.assertEqual(get_command(Color.RED, Color.BLUE),
                         Function._duplicate)
        self.assertEqual(get_command(Color.RED, Color.LIGHT_RED),
                         Function._pop)
        self.assertEqual(get_command(Color.RED, Color.DARK_RED),
                         Function._push)
        self.assertEqual(get_command(Color.BLUE, Color.LIGHT_RED),
                         Function._not)

    def test_functions_push(self):
        image_map = [[1, 2]]
        i = Interpreter('path', image_map, 1, 'None')
        i.previous_value = 23
        Function._push(i)
        self.assertEqual(i.stack.pop(), '23')

    def test_functions_pop(self):
        image_map = [[1, 2]]
        i = Interpreter('path', image_map, 1, 'None')
        i.previous_value = 23
        Function._push(i)
        Function._pop(i)
        self.assertEqual(i.stack, [])

    def test_functions_add(self):
        image_map = [[1, 2]]
        i = Interpreter('path', image_map, 1, 'None')
        i.previous_value = 23
        Function._push(i)
        i.previous_value = 32
        Function._push(i)
        Function._add(i)
        self.assertEqual(i.stack.pop(), '55')

    def test_functions_sub(self):
        image_map = [[1, 2]]
        i = Interpreter('path', image_map, 1, 'None')
        i.previous_value = 23
        Function._push(i)
        i.previous_value = 32
        Function._push(i)
        Function._subtract(i)
        self.assertEqual(i.stack.pop(), '-9')

    def test_functions_mul(self):
        image_map = [[1, 2]]
        i = Interpreter('path', image_map, 1, 'None')
        i.previous_value = 7
        Function._push(i)
        i.previous_value = 8
        Function._push(i)
        Function._multiply(i)
        self.assertEqual(i.stack.pop(), '56')

    def test_functions_div(self):
        image_map = [[1, 2],
                     [2, 1]]
        i = Interpreter('path', image_map, 1, 'None')
        i.previous_value = 40
        Function._push(i)
        i.previous_value = 8
        Function._push(i)
        Function._divide(i)
        self.assertEqual(i.stack.pop(), '5')

    def test_functions_mod(self):
        image_map = [[1, 2],
                     [2, 1]]
        i = Interpreter('path', image_map, 1, 'None')
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
        image_map = [[1, 2],
                     [2, 1]]
        i = Interpreter('path', image_map, 1, 'None')
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
        image_map = [[1, 2],
                     [2, 1]]
        i = Interpreter('path', image_map, 1, 'None')
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
        image_map = [[1, 2]]
        i = Interpreter('path', image_map, 1, 'None')
        i.previous_value = 23
        Function._push(i)
        Function._duplicate(i)
        self.assertEqual(i.stack.pop(), '23')
        self.assertEqual(i.stack.pop(), '23')

    def test_functions_switch(self):
        image_map = [[1, 2],
                     [2, 1]]
        i = Interpreter('path', image_map, 1, 'None')
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
        image_map = [[1, 2],
                     [2, 1]]
        i = Interpreter('path', image_map, 1, 'None')
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
        image_map = [[1, 2],
                     [2, 1]]
        i = Interpreter('path', image_map, 1, 'None')
        i.stack = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 5, 3]
        Function._roll(i)
        result = [1, 2, 3, 4, 5, 8, 9, 10, 6, 7]
        self.assertEqual(i.stack, result)
        Function._out_char(i)
        Function._out_num(i)


class InterpreterTest(unittest.TestCase):
    def test_hello_world(self):
        image_map = create_image_map(
            load_image("programs/HelloWorld.png"))

        class Test:
            def __init__(self, interpreter):
                self.interpreter = interpreter
                self.interpreter.output = self.out
                self.result = ''
                self.run()

            def out(self, res):
                self.result += res

            def run(self):
                while True:
                    self.interpreter.step()
                    if self.interpreter.state == State.END:
                        break

        i = Interpreter('path', image_map, 1, 'None')
        test = Test(i)

        self.assertEqual(test.result, 'Hello, World!')

    def test_breakpoint(self):
        image_map = [[1, 0, 0],
                     [2, 3, 1],
                     [0, 2, 1]]
        i = Interpreter('path', image_map, 1, 'None')
        i.image_map[3][2].is_stop = True
        self.assertEqual(i.state, State.RUNNING)
        i.step()
        i.step()
        i.step()
        i.step()
        self.assertEqual(i.state, State.STOPPED)


if __name__ == '__main__':
    unittest.main()

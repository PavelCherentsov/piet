from modules.components.Interpreter import Interpreter, State
from modules.ParseImage import create_image_map, load_image
import argparse
import sys


class Console:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.interpreter.input = self.console_input
        self.interpreter.output = self.console_print
        self.start_console()

    def start_console(self):
        while True:
            self.interpreter.step()
            if self.interpreter.state == State.END:
                break

    def console_print(self, res):
        print(res, sep=' ', end='', flush=True)

    def console_input(self):
        return input()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpreter Piet.')
    parser.add_argument('image', type=str,
                        help='path to the picture (program Piet) '
                             'relative to the file piet_interpr.py')
    parser.add_argument('--codel-size', metavar='N', type=int, default=0,
                        help='width of one codel')
    parser.add_argument('--mode', type=str,
                        choices=['None', 'white', 'black'],
                        default='None',
                        help='program operation mode')
    parser.add_argument('--trace', action='store_true',
                        help='Launching the graphical version '
                             'for debugging the program '
                             '(otherwise - the console version '
                             'without debugging)')
    args = parser.parse_args()
    try:
        image_map = create_image_map(load_image(args.image))
        if args.trace:
            from modules.Window import Window

            start = Window
        else:
            start = Console
        start(Interpreter(args.image, image_map, args.codel_size, args.mode))
    except (ValueError, IndexError) as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)

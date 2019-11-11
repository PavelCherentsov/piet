from modules.components.Interpreter import Interpreter
import argparse


def start_console(interpreter):
    while True:
        point = interpreter.start()
        if not interpreter.is_run:
            break
        if point is not None:
            print(point, sep=' ', end='', flush=True)
        if interpreter.is_in_num:
            try:
                interpreter.stack.append(str(int(input())))
            except TypeError:
                raise TypeError("Введите число")
            interpreter.is_in_num = False
        if interpreter.is_in_char:
            try:
                interpreter.stack.append(str(ord(input())))
            except TypeError:
                raise TypeError("Введите один символ")
            interpreter.is_in_char = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpreter Piet.')
    parser.add_argument('image', type=str,
                        help='path to the picture (program Piet) '
                             'relative to the file piet_interpr.py')
    parser.add_argument('--codel-size', metavar='N', type=int, default=0,
                        nargs='?',
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
    if args.trace:
        from modules.window import start_window as start_window
        start_window(Interpreter(args.image, args.codel_size, args.mode))
    else:
        start_console(Interpreter(args.image, args.codel_size, args.mode))

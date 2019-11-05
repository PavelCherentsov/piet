from modules.components.Interpreter import Interpreter
import argparse

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
    if not args.trace:
        from modules.console import start_console

        start_console(Interpreter(args.image, args.codel_size, args.mode))
    else:
        from modules.window import start_window

        start_window(Interpreter(args.image, args.codel_size, args.mode))

import sys
from PIL import Image
from modules.Interpreter import Interpreter


def main(image, trace=False):
    rgb_im = load_image(image)
    Interpreter(rgb_im, False, trace)


def load_image(image):
    return Image.open(image).convert('RGB')


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == '--help':
            print('\nПример запуска программы: '
                  '`py piet_interp.py HelloWorld.png`')
            print('Пример запуска c режимом пошагового исполнения: '
                  '`py piet_interp.py HelloWorld.png --trace`')
        else:
            main(sys.argv[1], False)
    elif len(sys.argv) == 3:
        if sys.argv[2] == '--trace':
            main(sys.argv[1], True)
    else:
        print('\nСправка по запуску: `py piet_interp.py --help``')

import sys
from modules.Point import Point
from modules.ColorTable import ColorDict
from PIL import Image
from modules.Interpreter import Interpreter


def main(image):
    im = Image.open(image)
    rgb_im = im.convert('RGB')
    image = []
    start_x = 0
    start_y = 0
    for x in range(im.width+2):
        image.append([])
    for x in range(im.width+2):
        for y in range(im.height+2):
            if x == 0 or y == 0 or x == im.width+1 or y == im.height+1:
                image[x].append('0x000000')
            else:
                r, g, b = rgb_im.getpixel((x-1, y-1))
                r = hex(r)
                g = hex(g)
                b = hex(b)
                if len(r) == 3:
                    r = r[:2] + "0" + r[2]
                if len(g) == 3:
                    g = g[:2] + "0" + g[2]
                if len(b) == 3:
                    b = b[:2] + "0" + b[2]
                check_correct_image(r[0:2]+(r[2:] + g[2:] + b[2:]).upper())
                image[x].append(r[0:2]+(r[2:] + g[2:] + b[2:]).upper())
    for x in range(im.width+2):
        for y in range(im.height+2):
            image[x][y] = Point(x, y, ColorDict[image[x][y]])
            if not (image[x][y].color in ['black', 'white']) and start_y == 0:
                start_x = x
                start_y = y


    Interpreter(image, start_x, start_y)


def check_correct_image(pixel):
    if not(pixel in ColorDict):
        print("Некорректная программа")
        sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1])

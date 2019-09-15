import sys
from Direction import Direction
from Point import Point
from ColorTable import ColorTable, ColorDict
from Stack import Stack
from PIL import Image
from Interpreter import Interpreter


def main(image):
    im = Image.open('image.png')
    rgb_im = im.convert('RGB')
    image = []
    for x in range(im.width):
        image.append([])
    for x in range(im.width):
        for y in range(im.height):
            r, g, b = rgb_im.getpixel((x, y))
            r = hex(r)
            g = hex(g)
            b = hex(b)
            if len(r) == 3:
                r = r[:2] + "0" + r[2]
            if len(g) == 3:
                g = g[:2] + "0" + g[2]
            if len(b) == 3:
                b = b[:2] + "0" + b[2]

            image[x].append(r + g[2:] + b[2:])

    for x in range(im.width):
        for y in range(im.height):
            image[x][y] = Point(x,y,image[x][y])
    inter = Interpreter(image)


if __name__ == "__main__":
    main(sys.argv[1])

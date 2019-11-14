from PIL import Image
from .components.ColorTable import COLORS_NUM


def load_image(image):
    return Image.open(image).convert('RGB')


def get_rgb(rgb_im, x, y):
    r, g, b = rgb_im.getpixel((x, y))
    return '0x' + ('%02x%02x%02x' % (r, g, b)).upper()


def create_image_map(rgb_im):
    image_map = []
    w = rgb_im.width
    h = rgb_im.height
    for x in range(w):
        image_map.append([])
    for x in range(w):
        for y in range(h):
            rgb = get_rgb(rgb_im, x, y)
            if rgb in COLORS_NUM:
                image_map[x].append(COLORS_NUM[rgb])
            else:
                image_map[x].append(-1)
    return image_map

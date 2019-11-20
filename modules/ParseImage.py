from PIL import Image


def load_image(image):
    return Image.open(image).convert('RGB')


def get_rgb(rgb_im, x, y):
    r, g, b = rgb_im.getpixel((x, y))
    return f'0x{r:02X}{g:02X}{b:02X}'


def create_image_map(rgb_im):
    image_map = []
    w = rgb_im.width
    h = rgb_im.height
    for x in range(w):
        image_map.append([])
    for x in range(w):
        for y in range(h):
            rgb = get_rgb(rgb_im, x, y)
            if rgb in COLORS:
                image_map[x].append(COLORS.index(rgb))
            else:
                image_map[x].append(rgb)
    return image_map


COLORS = ["0xFFFFFF", "0xFFC0C0", "0xFF0000", "0xC00000", "0xFFFFC0",
          "0xFFFF00", "0xC0C000", "0xC0FFC0", "0x00FF00", "0x00C000",
          "0xC0FFFF", "0x00FFFF", "0x00C0C0", "0xC0C0FF", "0x0000FF",
          "0x0000C0", "0xFFC0FF", "0xFF00FF", "0xC000C0", "0x000000"]

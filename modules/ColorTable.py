from .Function import FUNCTION_TABLE
from .Color import Color

COLOR_TABLE = [
    [Color.light_red, Color.light_yellow, Color.light_green,
     Color.light_cyan, Color.light_blue, Color.light_magenta],
    [Color.red, Color.yellow, Color.green,
     Color.cyan, Color.blue, Color.magenta],
    [Color.dark_red, Color.dark_yellow, Color.dark_green,
     Color.dark_cyan, Color.dark_blue, Color.dark_magenta],
]

COLORS = {
    "0xFFC0C0": Color.light_red,
    "0xFFFFC0": Color.light_yellow,
    "0xC0FFC0": Color.light_green,
    "0xC0FFFF": Color.light_cyan,
    "0xC0C0FF": Color.light_blue,
    "0xFFC0FF": Color.light_magenta,
    "0xFF0000": Color.red,
    "0xFFFF00": Color.yellow,
    "0x00FF00": Color.green,
    "0x00FFFF": Color.cyan,
    "0x0000FF": Color.blue,
    "0xFF00FF": Color.magenta,
    "0xC00000": Color.dark_red,
    "0xC0C000": Color.dark_yellow,
    "0x00C000": Color.dark_green,
    "0x00C0C0": Color.dark_cyan,
    "0x0000C0": Color.dark_blue,
    "0xC000C0": Color.dark_magenta,
    "0xFFFFFF": Color.white,
    "0x000000": Color.black,
    "None": "None"
}


def get_command(c1, c2):
    (c1_x, c1_y) = (0, 0)
    (c2_x, c2_y) = (0, 0)
    for i in range(3):
        for j in range(6):
            if COLOR_TABLE[i][j] == c1:
                (c1_x, c1_y) = (j, i)
            if COLOR_TABLE[i][j] == c2:
                (c2_x, c2_y) = (j, i)
    if c2_x - c1_x < 0:
        c2_x += 6
    if c2_y - c1_y < 0:
        c2_y += 3
    return FUNCTION_TABLE[c2_x - c1_x][c2_y - c1_y]

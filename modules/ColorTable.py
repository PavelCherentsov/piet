from .Function import FUNCTION_TABLE

COLORS = [
    ["light red", "light yellow", "light green",
     "light cyan", "light blue", "light magenta"],
    ["red", "yellow", "green", "cyan",  "blue", "magenta"],
    ["dark red", "dark yellow", "dark green",
     "dark cyan", "dark blue", "dark magenta"],
]

ColorDict = {
    "0xFFC0C0": "light red",
    "0xFFFFC0": "light yellow",
    "0xC0FFC0": "light green",
    "0xC0FFFF": "light cyan",
    "0xC0C0FF": "light blue",
    "0xFFC0FF": "light magenta",
    "0xFF0000": "red",
    "0xFFFF00": "yellow",
    "0x00FF00": "green",
    "0x00FFFF": "cyan",
    "0x0000FF": "blue",
    "0xFF00FF": "magenta",
    "0xC00000": "dark red",
    "0xC0C000": "dark yellow",
    "0x00C000": "dark green",
    "0x00C0C0": "dark cyan",
    "0x0000C0": "dark blue",
    "0xC000C0": "dark magenta",
    "0xFFFFFF": "white",
    "0x000000": "black",
    "None": "None"
}


def get_command(c1, c2):
    (c1_x, c1_y) = (0, 0)
    (c2_x, c2_y) = (0, 0)
    for i in range(3):
        for j in range(6):
            if COLORS[i][j] == c1:
                (c1_x, c1_y) = (j, i)
            if COLORS[i][j] == c2:
                (c2_x, c2_y) = (j, i)
    if c2_x - c1_x < 0:
        c2_x += 6
    if c2_y - c1_y < 0:
        c2_y += 3
    return FUNCTION_TABLE[c2_x - c1_x][c2_y - c1_y]

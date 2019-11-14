from enum import Enum


class Color(Enum):
    light_red = "0xFFC0C0",
    light_yellow = "0xFFFFC0",
    light_green = "0xC0FFC0",
    light_cyan = "0xC0FFFF",
    light_blue = "0xC0C0FF",
    light_magenta = "0xFFC0FF",
    red = "0xFF0000",
    yellow = "0xFFFF00",
    green = "0x00FF00",
    cyan = "0x00FFFF",
    blue = "0x0000FF",
    magenta = "0xFF00FF",
    dark_red = "0xC00000",
    dark_yellow = "0xC0C000",
    dark_green = "0x00C000",
    dark_cyan = "0x00C0C0",
    dark_blue = "0x0000C0",
    dark_magenta = "0xC000C0",
    white = "0xFFFFFF",
    black = "0x000000"


COLOR_TABLE = [
    [Color.light_red, Color.light_yellow, Color.light_green,
     Color.light_cyan, Color.light_blue, Color.light_magenta],
    [Color.red, Color.yellow, Color.green,
     Color.cyan, Color.blue, Color.magenta],
    [Color.dark_red, Color.dark_yellow, Color.dark_green,
     Color.dark_cyan, Color.dark_blue, Color.dark_magenta],
]

COLORS = {
    1: Color.light_red,
    4: Color.light_yellow,
    7: Color.light_green,
    10: Color.light_cyan,
    13: Color.light_blue,
    16: Color.light_magenta,
    2: Color.red,
    5: Color.yellow,
    8: Color.green,
    11: Color.cyan,
    14: Color.blue,
    17: Color.magenta,
    3: Color.dark_red,
    6: Color.dark_yellow,
    9: Color.dark_green,
    12: Color.dark_cyan,
    15: Color.dark_blue,
    18: Color.dark_magenta,
    0: Color.white,
    19: Color.black
}

COLORS_NUM = {
    "0xFFC0C0": 1,
    "0xFFFFC0": 4,
    "0xC0FFC0": 7,
    "0xC0FFFF": 10,
    "0xC0C0FF": 13,
    "0xFFC0FF": 16,
    "0xFF0000": 2,
    "0xFFFF00": 5,
    "0x00FF00": 8,
    "0x00FFFF": 11,
    "0x0000FF": 14,
    "0xFF00FF": 17,
    "0xC00000": 3,
    "0xC0C000": 6,
    "0x00C000": 9,
    "0x00C0C0": 12,
    "0x0000C0": 15,
    "0xC000C0": 18,
    "0xFFFFFF": 0,
    "0x000000": 19,
    "None": "None"
}

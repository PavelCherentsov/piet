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

from enum import Enum


class Color(Enum):
    WHITE = 0
    LIGHT_RED = 1
    RED = 2
    DARK_RED = 3
    LIGHT_YELLOW = 4
    YELLOW = 5
    DARK_YELLOW = 6
    LIGHT_GREEN = 7
    GREEN = 8
    DARK_GREEN = 9
    LIGHT_CYAN = 10
    CYAN = 11
    DARK_CYAN = 12
    LIGHT_BLUE = 13
    BLUE = 14
    DARK_BLUE = 15
    LIGHT_MAGENTA = 16
    MAGENTA = 17
    DARK_MAGENTA = 18
    BLACK = 19


COLOR_TABLE = [
    [Color.LIGHT_RED, Color.LIGHT_YELLOW, Color.LIGHT_GREEN,
     Color.LIGHT_CYAN, Color.LIGHT_BLUE, Color.LIGHT_MAGENTA],
    [Color.RED, Color.YELLOW, Color.GREEN,
     Color.CYAN, Color.BLUE, Color.MAGENTA],
    [Color.DARK_RED, Color.DARK_YELLOW, Color.DARK_GREEN,
     Color.DARK_CYAN, Color.DARK_BLUE, Color.DARK_MAGENTA]]

from .Color import Color


ColorTable = [
    [(0xFFC0C0, "light red"), (0xFFFFC0, "light yellow"), (0xC0FFC0, "light green"),
     (0xC0FFFF, "light cyan"), (0xC0C0FF, "light blue"), (0xFFC0FF, "light magenta")],
    [(0xFF0000, "red"), (0xFFFF00, "yellow"), (0x00FF00, "green"),
     (0x00FFFF, "cyan"), (0x0000FF, "blue"), (0xFF00FF, "magenta")],
    [(0xC00000, "dark red"), (0xC0C000, "dark yellow"), (0x00C000, "dark green"),
     (0x00C0C0, "dark cyan"), (0x0000C0, "dark blue"), (0xC000C0, "dark magenta")],
    [(0xFFFFFF, "white"), (0x000000, "black")]
]

ColorDict = {
        "0xFFC0C0": Color("light red", "red", "red", "dark red", "light yellow"),
        "0xFFFFC0": Color("light yellow", "yellow", "yellow", "dark yellow", "light green"),
        "0xC0FFC0": Color("light green", "green", "green", "dark green", "light cyan"),
        "0xC0FFFF": Color("light cyan", "cyan", "cyan", "dark cyan", "light blue"),
        "0xC0C0FF": Color("light blue", "blue", "blue", "dark blue", "light magenta"),
        "0xFFC0FF": Color("light magenta", "magenta", "magenta", "dark magenta", "light red"),
        "0xFF0000": Color("red", "red", "dark magenta", "light magenta", "yellow"),
        "0xFFFF00": Color("yellow", "yellow", "dark yellow", "light yellow", "green"),
        "0x00FF00": Color("green", "green", "dark green", "light green", "cyan"),
        "0x00FFFF": Color("cyan", "cyan", "dark cyan", "light cyan", "blue"),
        "0x0000FF": Color("blue", "blue", "dark blue", "light blue", "magenta"),
        "0xFF00FF": Color("magenta", "magenta", "dark magenta", "light magenta", "red"),
        "0xC00000": "dark red",
        "0xC0C000": "dark yellow",
        "0x00C000": "dark green",
        "0x00C0C0": "dark cyan",
        "0x0000C0": "dark blue",
        "0xC000C0": "dark magenta",
        "0xFFFFFF": "white",
        "0x000000": "black"
}
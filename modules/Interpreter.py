from CodelChooser import CodelChooser
from DirectionPointer import DirectionPointer


class Interpreter:
    def __init__(self, image):
        self.x = 0
        self.y = 0
        self.direction_pointer = DirectionPointer()
        self.codel_chooser = CodelChooser()
        self.points = image
        self.previos = None


    def initialize_block(self):
        self.points.append()

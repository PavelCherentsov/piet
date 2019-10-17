from PIL import Image
from modules.Interpreter import Interpreter
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QFont
import sys
import argparse


WINDOW_WIDTH = 0
WINDOW_HEIGHT = 0


class Example(QWidget):
    def __init__(self, image, codel_size, mode):
        super().__init__()
        self.image = image
        self.codel_size = codel_size
        self.mode = mode
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle('Piet Interpreter')
        self.setWindowIcon(QIcon('icon.png'))

        label = QLabel(self)
        qpm = QPixmap(self.image)
        qpm = qpm.scaled(WINDOW_WIDTH // 2, WINDOW_WIDTH // 2, 1)

        label.setPixmap(qpm)
        label.setGeometry(50, 50, qpm.width(), qpm.height())

        self.interpreter = Interpreter(
            self.load_image(self.image), self.codel_size, self.mode)

        self.dx = (WINDOW_WIDTH // 2) / (len(self.interpreter.image_map) - 2)

        self.button_run = QPushButton('Run', self)
        self.button_run.move(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 150)
        self.button_run.clicked[bool].connect(self.main)

        self.button_next = QPushButton('Next Step', self)
        self.button_next.move(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 100)
        self.button_next.clicked[bool].connect(self.main_trace)


        self.info_stack = QLabel(self)
        self.info_stack.setText(str(self.interpreter.stack))
        self.info_stack.setFont(QFont("Arial", 14))
        self.info_stack.setMinimumWidth(1000)
        self.info_stack.setVisible(True)
        self.info_stack.move(WINDOW_WIDTH // 2 + 100, 100)

        self.info_function = QLabel(self)
        self.info_function.setText("Function: ")
        self.info_function.setFont(QFont("Arial", 14))
        self.info_function.setMinimumWidth(1000)
        self.info_function.setVisible(True)
        self.info_function.move(WINDOW_WIDTH // 2 + 100, 50)

        self.info_output = QLabel(self)
        self.info_output.setText("Output: ")
        self.info_output.setFont(QFont("Arial", 14))
        self.info_output.setMinimumWidth(1000)
        self.info_output.setVisible(True)
        self.info_output.move(WINDOW_WIDTH // 2 + 100, 150)

        self.star = QLabel(self)
        self.star.setPixmap(QPixmap('star.png').scaled(self.dx, self.dx))
        self.star.move(50 + (self.interpreter.x - 1) * self.dx,
                       50 + (self.interpreter.y - 1) * self.dx)
        self.show()

    def main(self):
        while True:
            if not self.interpreter.start():
                break
            self.print_info()
            self.button_run.setEnabled(False)
            self.button_next.setEnabled(False)

    def main_trace(self):
        if not self.interpreter.start():
            self.button_run.setEnabled(False)
            self.button_next.setEnabled(False)
        self.print_info()


    def load_image(self, image):
        return Image.open(image).convert('RGB')

    def print_info(self):
        self.star.move(50 + (self.interpreter.x - 1) * self.dx,
                       50 + (self.interpreter.y - 1) * self.dx)
        self.info_stack.setText(str(self.interpreter.stack))
        if self.interpreter.command is None:
            self.info_function.setText(
                "Function: ")
        else:
            self.info_function.setText(
                "Function: " + self.interpreter.command.__name__[1:])
        self.info_output.setText("Output: " + self.interpreter.out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpreter Piet.')
    parser.add_argument('image', type=str,
                        help='path to the picture (program Piet) '
                             'relative to the file piet_interpr.py')
    parser.add_argument('codel_size', type=int, default=0, nargs='?',
                        help='width of one codel (or to automatically '
                             'detect the codel, enter: 0)')
    parser.add_argument('mode', type=int, metavar='mode', choices=[0, 1, 2],
                        default=0, nargs='?',
                        help='program operation mode: 0 - The program does '
                             'not work with an undefined image, 1 - Invalid '
                             'pixels are replaced with white, 2 - Invalid '
                             'pixels are replaced with black')
    args = parser.parse_args()
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    WINDOW_WIDTH = rect.width() - 200
    WINDOW_HEIGHT = rect.height() - 100
    e = Example(args.image, args.codel_size, args.mode)
    sys.exit(app.exec_())

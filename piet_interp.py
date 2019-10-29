from PIL import Image
from modules.Interpreter import Interpreter
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, \
    QListWidget, QTextEdit, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
import sys
import argparse

WINDOW_WIDTH = 0
WINDOW_HEIGHT = 0
MainInterpreter = None


class Window(QWidget):
    def __init__(self, image, codel_size, mode):
        super().__init__()
        self.image = image
        self.codel_size = codel_size
        self.mode = mode

        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle('Piet Interpreter')
        self.setWindowIcon(QIcon('icon.png'))

        label = QLabel(self)
        qpm = QPixmap(self.image)
        qpm = qpm.scaled(WINDOW_WIDTH // 2, WINDOW_WIDTH // 2, 1)

        label.setPixmap(qpm)
        label.setGeometry(50, 50, qpm.width(), qpm.height())
        label.scroll(50, 50)
        global MainInterpreter
        MainInterpreter = Interpreter(
            load_image(self.image), self.codel_size, self.mode)

        self.dx = (WINDOW_WIDTH // 2) / (len(MainInterpreter.image_map) - 2)

        info_stack_text = QLabel(self)
        info_stack_text.setText("Stack: ")
        info_stack_text.setFont(QFont("Arial", 14))
        info_stack_text.setVisible(True)
        info_stack_text.move(WINDOW_WIDTH // 2 + WINDOW_WIDTH // 4 +
                             WINDOW_WIDTH // 8 - 70, 50)

        self.info_stack = QListWidget(self)
        self.info_stack.setFixedWidth(WINDOW_WIDTH // 4 - 100 - 50)
        self.info_stack.setFixedHeight(WINDOW_HEIGHT // 4 * 3 - 100)
        self.info_stack.move(WINDOW_WIDTH // 2 + WINDOW_WIDTH // 4 + 50, 100)
        self.info_stack.setFont(QFont("Arial", 14))

        self.info_stack.addItems(MainInterpreter.stack.stack)

        self.info_function = QLabel(self)
        self.info_function.setText("Function: ")
        self.info_function.setFont(QFont("Arial", 14))
        self.info_function.setMinimumWidth(1000)
        self.info_function.setVisible(True)
        self.info_function.move(WINDOW_WIDTH // 2 + WINDOW_WIDTH // 4 - 100, 0)

        info_input_text = QLabel(self)
        info_input_text.setText("Input: ")
        info_input_text.setFont(QFont("Arial", 14))
        info_input_text.setMinimumWidth(1000)
        info_input_text.setVisible(True)
        info_input_text.move(WINDOW_WIDTH // 2 + 100, WINDOW_HEIGHT - 100)

        self.info_input = QLineEdit(self)
        self.info_input.setFixedWidth(200)
        self.info_input.setFixedHeight(50)
        self.info_input.move(WINDOW_WIDTH // 2 + 160, WINDOW_HEIGHT - 100 - 10)
        self.info_input.setReadOnly(False)
        self.info_input.setEnabled(False)
        self.info_input.setFont(QFont("Arial", 14))
        self.info_input.setAlignment(Qt.AlignCenter)

        info_output_text = QLabel(self)
        info_output_text.setText("Output: ")
        info_output_text.setFont(QFont("Arial", 14))
        info_output_text.setVisible(True)
        info_output_text.move(WINDOW_WIDTH // 2 +
                              WINDOW_WIDTH // 8 - 70, 50)

        self.info_output = QTextEdit(self)
        self.info_output.setFixedWidth(WINDOW_WIDTH // 4 - 100 - 50)
        self.info_output.setFixedHeight(WINDOW_HEIGHT // 4 * 3 - 100)
        self.info_output.move(WINDOW_WIDTH // 2 + 100, 100)
        self.info_output.setReadOnly(True)
        self.info_output.setFont(QFont("Arial", 14))
        self.info_output.setAlignment(Qt.AlignTop)

        self.star = QLabel(self)
        self.star.setPixmap(QPixmap('star.png').scaled(self.dx, self.dx))
        self.star.move(50 + (MainInterpreter.x - 1) * self.dx,
                       50 + (MainInterpreter.y - 1) * self.dx)

        self.button_run = QPushButton('Run', self)
        self.button_run.move(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 150)
        self.button_run.clicked[bool].connect(self.main)

        self.button_next = QPushButton('Next Step', self)
        self.button_next.move(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 100)
        self.button_next.clicked[bool].connect(self.main_trace)

        self.restart_button = QPushButton('Restart', self)
        self.restart_button.move(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 50)
        self.restart_button.clicked[bool].connect(self.restart)

        self.show()

    def restart(self):
        global MainInterpreter
        MainInterpreter = Interpreter(
            load_image(self.image), self.codel_size, self.mode)
        self.print_info()
        self.info_input.clear()
        self.info_input.setEnabled(False)
        self.button_next.setEnabled(True)
        self.button_run.setEnabled(True)

    def main(self):
        while True:
            if self.main_trace():
                break
            if MainInterpreter.command is not None:
                if MainInterpreter.command.__name__[1:] in ['in_num',
                                                            'in_char']:
                    break
            self.print_info()

    def main_trace(self):
        self.info_input.setEnabled(False)
        text = self.info_input.text()
        if MainInterpreter.command is not None:
            if MainInterpreter.command.__name__[1:] == 'in_num':
                MainInterpreter.stack.push(text)
            if MainInterpreter.command.__name__[1:] == 'in_char':
                MainInterpreter.stack.push(str(ord(text)))

        self.info_input.clear()
        point = MainInterpreter.start()
        if type(point) is bool:
            if not point:
                self.button_run.setEnabled(False)
                self.button_next.setEnabled(False)
                return True
        self.print_info()
        if MainInterpreter.command is not None:
            if MainInterpreter.command.__name__[1:] in ['in_num', 'in_char']:
                self.info_input.setEnabled(True)

    def print_info(self):
        self.star.move(50 + (MainInterpreter.x - 1) * self.dx,
                       50 + (MainInterpreter.y - 1) * self.dx)
        self.info_stack.clear()
        self.info_stack.addItems(MainInterpreter.stack.stack)
        if MainInterpreter.command is None:
            self.info_function.setText(
                "Function: ")
        else:
            self.info_function.setText(
                "Function: " + MainInterpreter.command.__name__[1:])
        self.info_output.setText(MainInterpreter.out)


def load_image(image):
    return Image.open(image).convert('RGB')


def start():
    while True:
        point = MainInterpreter.start()
        if (type(point) is not bool) and (point is not None):
            print(point, sep=' ', end='', flush=True)
        if type(point) is bool:
            if not point:
                break
        if MainInterpreter.command is not None:
            if MainInterpreter.command.__name__[1:] == 'in_num':
                MainInterpreter.stack.push(input())
            if MainInterpreter.command.__name__[1:] == 'in_char':
                MainInterpreter.stack.push(str(ord(input())))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpreter Piet.')
    parser.add_argument('image', type=str,
                        help='path to the picture (program Piet) '
                             'relative to the file piet_interpr.py')
    parser.add_argument('--codel_size', metavar='N', type=int, default=0,
                        nargs='?',
                        help='width of one codel (or to automatically '
                             'detect the codel, enter: 0)')
    parser.add_argument('--mode', type=str,
                        choices=['ExecutionAnyway',
                                 'ReplacementForWhite',
                                 'ReplacementForBlack'],
                        default='ExecutionAnyway',
                        help='program operation mode: '
                             'ExecutionAnyway - The program does '
                             'not work with an undefined image, '
                             'ReplacementForWhite - Invalid '
                             'pixels are replaced with white, '
                             'ReplacementForBlack - Invalid '
                             'pixels are replaced with black')
    parser.add_argument('--trace', action='store_true',
                        help='Launching the graphical version '
                             'for debugging the program '
                             '(otherwise - the console version '
                             'without debugging)')
    args = parser.parse_args()
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    WINDOW_WIDTH = rect.width() - 200
    WINDOW_HEIGHT = rect.height() - 100
    if not args.trace:
        MainInterpreter = Interpreter(load_image(args.image), args.codel_size,
                                      args.mode)
        start()
    else:
        e = Window(args.image, args.codel_size, args.mode)
        sys.exit(app.exec_())

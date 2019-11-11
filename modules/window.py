from modules.components.Interpreter import Interpreter
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QListWidget, QTextEdit, QLineEdit)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
import sys


class Window(QWidget):
    def __init__(self, interpreter, width, height):
        super().__init__()
        self.image = interpreter.image
        self.image_path = interpreter.image_path
        self.codel_size = interpreter.codel_size
        self.mode = interpreter.mode
        self.interpreter = interpreter
        self.setGeometry(100, 100, width, height)
        self.setFixedSize(width, height)
        self.setWindowTitle('Piet Interpreter')
        self.setWindowIcon(QIcon('icon.png'))
        self.bugs_count = 20

        label = QLabel(self)
        qpm = QPixmap(self.interpreter.image_path)
        qpm = qpm.scaled(width // 2, height, 1)

        label.setPixmap(qpm)
        label.setGeometry(50, 50, qpm.width(), qpm.height())

        self.dx = (width // 2) / (len(self.interpreter.image_map) - 2)

        info_stack_text = QLabel(self)
        info_stack_text.setText("Stack: ")
        info_stack_text.setFont(QFont("Arial", 14))
        info_stack_text.setVisible(True)
        info_stack_text.move(width // 2 + width // 4 +
                             width // 8 - 70, 50)

        self.info_stack = QListWidget(self)
        self.info_stack.setFixedWidth(width // 4 - 100 - 50)
        self.info_stack.setFixedHeight(height // 4 * 3 - 100)
        self.info_stack.move(width // 2 + width // 4 + 50, 100)
        self.info_stack.setFont(QFont("Arial", 14))

        self.info_stack.addItems(self.interpreter.stack)

        self.info_function = QLabel(self)
        self.info_function.setText("Function: ")
        self.info_function.setFont(QFont("Arial", 14))
        self.info_function.setMinimumWidth(1000)
        self.info_function.setVisible(True)
        self.info_function.move(width // 2 + width // 4 - 100, 0)

        info_input_text = QLabel(self)
        info_input_text.setText("Input: ")
        info_input_text.setFont(QFont("Arial", 14))
        info_input_text.setMinimumWidth(1000)
        info_input_text.setVisible(True)
        info_input_text.move(width // 2 + 100, height - 100)

        self.info_input = QLineEdit(self)
        self.info_input.setFixedWidth(200)
        self.info_input.setFixedHeight(50)
        self.info_input.move(width // 2 + 160, height - 100 - 10)
        self.info_input.setReadOnly(False)
        self.info_input.setEnabled(False)
        self.info_input.setFont(QFont("Arial", 14))
        self.info_input.setAlignment(Qt.AlignCenter)

        info_output_text = QLabel(self)
        info_output_text.setText("Output: ")
        info_output_text.setFont(QFont("Arial", 14))
        info_output_text.setVisible(True)
        info_output_text.move(width // 2 +
                              width // 8 - 70, 50)

        self.info_output = QTextEdit(self)
        self.info_output.setFixedWidth(width // 4 - 100 - 50)
        self.info_output.setFixedHeight(height // 4 * 3 - 100)
        self.info_output.move(width // 2 + 100, 100)
        self.info_output.setReadOnly(True)
        self.info_output.setFont(QFont("Arial", 14))
        self.info_output.setAlignment(Qt.AlignTop)

        self.star = QLabel(self)
        self.star.setPixmap(QPixmap('star.png').scaled(self.dx, self.dx))
        self.star.move(50 + (self.interpreter.x - 1) * self.dx,
                       50 + (self.interpreter.y - 1) * self.dx)

        self.button_run = QPushButton('Run', self)
        self.button_run.move(width - 150, height - 150)
        self.button_run.clicked[bool].connect(self.main)

        self.button_next = QPushButton('Next Step', self)
        self.button_next.move(width - 150, height - 100)
        self.button_next.clicked[bool].connect(self.main_trace)

        self.restart_button = QPushButton('Restart', self)
        self.restart_button.move(width - 150, height - 50)
        self.restart_button.clicked[bool].connect(self.restart)

        self.bugs = []

        for i in range(self.bugs_count):
            bug = QLabel(self)
            bug.setPixmap(QPixmap('bug.png').scaled(self.dx, self.dx))
            bug.move(-1000, -1000)
            self.bugs.append(bug)

        self.show()

    def mousePressEvent(self, event):
        x = int((event.x() - 50) // self.dx + 1)
        y = int((event.y() - 50) // self.dx + 1)
        try:
            if x in [0, len(self.interpreter.image_map) - 1] or \
                    y in [0, len(self.interpreter.image_map[0]) - 1]:
                raise IndexError
            if self.bugs_count > 0:
                if not self.interpreter.image_map[x][y].is_stop:
                    self.interpreter.image_map[x][y].is_stop = True
                    self.bugs_count -= 1
                    bug = self.bugs[self.bugs_count]
                    bug.move(50 + (x - 1) * self.dx,
                             50 + (y - 1) * self.dx)
                else:
                    self.interpreter.image_map[x][y].is_stop = False
                    for e in self.bugs:
                        if (e.x(), e.y()) == \
                                (int(50 + (x - 1) * self.dx),
                                 int(50 + (y - 1) * self.dx)):
                            self.bugs_count += 1
                            e.move(-1000, -1000)
                            break
        except IndexError:
            pass

    def restart(self):
        self.interpreter = Interpreter(self.image_path, self.codel_size,
                                       self.mode)
        self.print_info()
        self.info_input.clear()
        self.info_input.setEnabled(False)
        self.button_next.setEnabled(True)
        self.button_run.setEnabled(True)
        for e in self.bugs:
            e.move(-1000, -1000)
        for e in self.interpreter.image_map:
            for j in e:
                j.is_stop = False


    def main(self):
        while True:
            if self.main_trace():
                break
            if self.interpreter.is_in_char or self.interpreter.is_in_num:
                break
            self.print_info()

    def main_trace(self):
        self.info_input.setEnabled(False)
        if self.interpreter.is_in_num:
            try:
                if self.info_input.text() == '':
                    raise TypeError("Введите число")
                else:
                    self.interpreter.stack.append(self.info_input.text())
            except TypeError:
                raise TypeError("Введите число")
            self.interpreter.is_in_num = False
        if self.interpreter.is_in_char:
            try:
                if self.info_input.text() == '':
                    raise TypeError("Введите один символ")
                else:
                    self.interpreter.stack.append(str(ord(self.info_input.text())))
            except TypeError:
                raise TypeError("Введите один символ")
            self.interpreter.is_in_char = False
        self.info_input.clear()

        self.interpreter.start()

        if not self.interpreter.is_run:
            self.button_run.setEnabled(False)
            self.button_next.setEnabled(False)
            return True
        self.print_info()

        if self.interpreter.is_in_char or self.interpreter.is_in_num:
            self.info_input.setEnabled(True)

        if self.interpreter.stop:
            self.interpreter.stop = False
            for e in self.interpreter.block:
                if e.is_stop:
                    e.is_stop = False
                    for b in self.bugs:
                        if (b.x(), b.y()) == \
                                (int(50 + (e.x - 1) * self.dx),
                                 int(50 + (e.y - 1) * self.dx)):
                            self.bugs_count += 1
                            b.move(-1000, -1000)
            return True

    def print_info(self):
        self.star.move(50 + (self.interpreter.x - 1) * self.dx,
                       50 + (self.interpreter.y - 1) * self.dx)
        self.info_stack.clear()
        self.info_stack.addItems(self.interpreter.stack)
        if self.interpreter.command is None:
            self.info_function.setText("Function: ")
        else:
            self.info_function.setText("Function: " +
                                       self.interpreter.command.__name__[1:])
        self.info_output.setText(self.interpreter.out)


def start_window(interpreter):
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    e = Window(interpreter, rect.width() - 200, rect.height() - 100)
    sys.exit(app.exec_())

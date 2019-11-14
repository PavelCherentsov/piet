from modules.components.Interpreter import Interpreter
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QListWidget, QTextEdit, QInputDialog)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
import sys


class Window(QWidget):
    def __init__(self, interpreter, width, height):
        super().__init__()
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
        qpm = qpm.scaled(width // 2 + width // 4 - 50, height - 300, 1)

        label.setPixmap(qpm)
        label.setGeometry(50, 100, qpm.width(), qpm.height())

        self.dx = max(label.width(), label.height()) / (
                len(self.interpreter.image_map) - 2)

        info_stack_text = QLabel(self)
        info_stack_text.setText("Stack: ")
        info_stack_text.setFont(QFont("Arial", 14))
        info_stack_text.setVisible(True)
        info_stack_text.move(width // 2 + width // 4 +
                             width // 8 - 70, 60)

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
        self.info_function.move(width // 2 - 100, 50)

        self.info_output = QTextEdit(self)
        self.info_output.setFixedWidth(width - 200)
        self.info_output.setFixedHeight(100)
        self.info_output.move(100, height - 150)
        self.info_output.setReadOnly(True)
        self.info_output.setFont(QFont("Arial", 14))
        self.info_output.setAlignment(Qt.AlignTop)

        self.star = QLabel(self)
        self.star.setPixmap(QPixmap('star.png').scaled(self.dx, self.dx))
        self.star.move(50 + (self.interpreter.x - 1) * self.dx,
                       100 + (self.interpreter.y - 1) * self.dx)

        self.button_run = QPushButton('Run', self)
        self.button_run.move(50, 0)
        self.button_run.setFixedSize(width // 3 - 100, 50)
        self.button_run.clicked[bool].connect(self.main)

        self.button_next = QPushButton('Next Step', self)
        self.button_next.setFixedSize(width // 3 - 100, 50)
        self.button_next.move((width + 100) // 3, 0)
        self.button_next.clicked[bool].connect(self.main_trace)

        self.restart_button = QPushButton('Restart', self)
        self.restart_button.setFixedSize(width // 3 - 100, 50)
        self.restart_button.move(2 * width // 3, 0)
        self.restart_button.clicked[bool].connect(self.restart)

        self.bugs = []

        for i in range(self.bugs_count):
            bug = QLabel(self)
            bug.setPixmap(QPixmap('bug.png').scaled(self.dx, self.dx))
            bug.move(-1000, -1000)
            self.bugs.append(bug)

        self.show()

    def show_dialog(self, title):
        text, ok = QInputDialog.getText(self, 'Input', title)
        if ok:
            return str(text)

    def mousePressEvent(self, event):
        x = int((event.x() - 50) // self.dx + 1)
        y = int((event.y() - 100) // self.dx + 1)
        try:
            if x <= 0 or \
                    y <= 0 or \
                    x >= len(self.interpreter.image_map) - 1 or \
                    y >= len(self.interpreter.image_map[0]) - 1:
                raise IndexError
            if self.bugs_count > 0:
                if not self.interpreter.image_map[x][y].is_stop:
                    self.interpreter.image_map[x][y].is_stop = True
                    self.bugs_count -= 1
                    bug = self.bugs[self.bugs_count]
                    bug.move(50 + (x - 1) * self.dx,
                             100 + (y - 1) * self.dx)
                else:
                    self.interpreter.image_map[x][y].is_stop = False
                    for e in self.bugs:
                        if (e.x(), e.y()) == \
                                (int(50 + (x - 1) * self.dx),
                                 int(100 + (y - 1) * self.dx)):
                            self.bugs_count += 1
                            e.move(-1000, -1000)
                            break
        except IndexError:
            pass

    def restart(self):
        self.interpreter = Interpreter(self.image_path,
                                       self.interpreter.image_map_start,
                                       self.codel_size,
                                       self.mode)
        self.print_info()
        self.button_next.setEnabled(True)
        self.button_run.setEnabled(True)
        for e in self.bugs:
            e.move(-1000, -1000)
        for e in self.interpreter.image_map:
            for j in e:
                j.is_stop = False
        self.bugs_count = 20

    def main(self):
        while True:
            if self.main_trace():
                break
            if self.interpreter.is_in_char or self.interpreter.is_in_num:
                break
            self.print_info()

    def main_trace(self):
        self.interpreter.start()

        if self.interpreter.is_in_num:
            e = self.show_dialog('Input number:')
            try:
                self.interpreter.stack.append(str(int(e)))
            except ValueError:
                raise ValueError('Invalid input')
            self.interpreter.is_in_num = False
        if self.interpreter.is_in_char:
            e = self.show_dialog('Input char:')
            try:
                self.interpreter.stack.append(str(ord(e)))
            except ValueError:
                raise ValueError('Invalid input')
            self.interpreter.is_in_char = False

        if not self.interpreter.is_run:
            self.button_run.setEnabled(False)
            self.button_next.setEnabled(False)
            return True
        self.print_info()

        if self.interpreter.stop:
            self.interpreter.stop = False
            for e in self.interpreter.block:
                if e.is_stop:
                    e.is_stop = False
                    for b in self.bugs:
                        if (b.x(), b.y()) == \
                                (int(50 + (e.x - 1) * self.dx),
                                 int(100 + (e.y - 1) * self.dx)):
                            self.bugs_count += 1
                            b.move(-1000, -1000)
            return True

    def print_info(self):
        self.star.move(50 + (self.interpreter.x - 1) * self.dx,
                       100 + (self.interpreter.y - 1) * self.dx)
        self.info_stack.clear()
        self.info_stack.addItems(self.interpreter.stack)
        if self.interpreter.command is None:
            self.info_function.setText("Function: ")
        else:
            self.info_function.setText("Function: " +
                                       self.interpreter.command.name)
        self.info_output.setText(self.interpreter.out)


def start_window(interpreter):
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    e = Window(interpreter, rect.width() - 200, rect.height() - 100)
    sys.exit(app.exec_())

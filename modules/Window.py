from modules.components.Interpreter import Interpreter, State
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QListWidget, QTextEdit, QInputDialog,
                             QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
import sys


class Application(QWidget):
    def __init__(self, interpreter, width, height):
        super().__init__()
        self.image_path = interpreter.image_path
        self.codel_size = interpreter.codel_size
        self.mode = interpreter.mode
        self.interpreter = interpreter

        self.interpreter.input = self.show_input
        self.interpreter.output = self.print_info

        self.setGeometry(100, 100, width, height)
        self.setFixedSize(width, height)
        self.setWindowTitle('Piet Interpreter')
        self.setWindowIcon(QIcon('icon.png'))

        label = QLabel(self)
        qpm = QPixmap(self.interpreter.image_path)
        qpm = qpm.scaled(width // 2 + width // 4 - 50, height - 300, 1)

        label.setPixmap(qpm)
        label.setGeometry(50, 100, qpm.width(), qpm.height())

        self.dx = label.width() / (
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

        self.bugs_count = \
            self.window_input_bugs('How many breakpoints?\n'
                                   'Enter the number of breakpoints')

        for i in range(self.bugs_count):
            bug = QLabel(self)
            bug.setPixmap(QPixmap('bug.png').scaled(self.dx, self.dx))
            bug.move(0, 0)
            bug.setVisible(False)
            self.bugs.append(bug)

        self.print_info('')

        self.show()

    def window_input_bugs(self, title):
        text, ok = QInputDialog.getText(self, 'Hello!', title)
        if ok:
            try:
                return int(text)
            except ValueError:
                self.window_input_bugs(title)
        else:
            sys.exit(0)

    def show_dialog(self, title):
        text, ok = QInputDialog.getText(self, 'Input', title)
        if ok:
            return str(text)
        else:
            sys.exit(0)

    def show_exception(self, ex):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Warning!!!")
        msg.setText(str(ex))
        msg.setStandardButtons(QMessageBox.Close)
        retval = msg.exec_()
        sys.exit(1)

    def mousePressEvent(self, event):
        x = int((event.x() - 50) // self.dx + 1)
        y = int((event.y() - 100) // self.dx + 1)
        try:
            if not (0 < x < len(self.interpreter.image_map) - 1) or \
                    not (0 < y < len(self.interpreter.image_map[0]) - 1):
                raise IndexError
            if self.bugs_count:
                if not self.interpreter.image_map[x][y].is_stop:
                    self.interpreter.image_map[x][y].is_stop = True
                    self.bugs_count -= 1
                    bug = self.bugs[self.bugs_count]
                    bug.move(50 + (x - 1) * self.dx,
                             100 + (y - 1) * self.dx)
                    bug.setVisible(True)
                else:
                    self.interpreter.image_map[x][y].is_stop = False
                    for e in self.bugs:
                        if (e.x(), e.y()) == \
                                (int(50 + (x - 1) * self.dx),
                                 int(100 + (y - 1) * self.dx)):
                            self.bugs_count += 1
                            e.move(0, 0)
                            e.setVisible(False)
                            break
        except IndexError:
            return

    def restart(self):
        self.interpreter = Interpreter(self.image_path,
                                       self.interpreter.image_map_start,
                                       self.codel_size,
                                       self.mode)
        self.interpreter.input = self.show_input
        self.interpreter.output = self.print_info
        self.print_info('')
        self.info_output.clear()
        self.button_next.setEnabled(True)
        self.button_run.setEnabled(True)
        for e in self.bugs:
            e.move(0, 0)
            e.setVisible(False)
        for e in self.interpreter.image_map:
            for j in e:
                j.is_stop = False
        self.bugs_count = 1000

    def show_input(self):
        if self.interpreter.is_in_num:
            return self.show_dialog('Input number:')
        if self.interpreter.is_in_char:
            return self.show_dialog('Input char:')

    def main(self):
        while True:
            if self.main_trace():
                break

    def main_trace(self):
        try:
            e = self.interpreter.step()
        except Exception as ex:
            self.show_exception(ex)
        if e is None:
            e = ''
        self.print_info(e)

        if self.interpreter.state == State.END:
            self.button_run.setEnabled(False)
            self.button_next.setEnabled(False)
            return True

        if self.interpreter.state == State.STOPPED:
            self.interpreter.state = State.RUNNING
            for e in self.interpreter.block:
                if e.is_stop:
                    e.is_stop = False
                    for b in self.bugs:
                        if (b.x(), b.y()) == \
                                (int(50 + (e.x - 1) * self.dx),
                                 int(100 + (e.y - 1) * self.dx)):
                            self.bugs_count += 1
                            b.move(0, 0)
                            b.setVisible(False)
            return True

    def print_info(self, e):
        self.star.move(50 + (self.interpreter.x - 1) * self.dx,
                       100 + (self.interpreter.y - 1) * self.dx)
        self.info_stack.clear()
        self.info_stack.addItems(self.interpreter.stack)
        if self.interpreter.next_command is not None:
            self.info_function.setText("Next Function: " +
                                       self.interpreter.next_command.name)
        text = self.info_output.toPlainText() + e
        self.info_output.setText(text)


class Window:
    def __init__(self, interpreter):
        app = QApplication(sys.argv)
        screen = app.primaryScreen()
        rect = screen.availableGeometry()
        self.app = Application(interpreter, rect.width() - 200,
                               rect.height() - 100)
        sys.exit(app.exec_())

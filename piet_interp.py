from PIL import Image
from modules.Interpreter import Interpreter
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QFont
import sys


def load_image(image):
    return Image.open(image).convert('RGB')


class Example(QWidget):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1500, 900)
        self.setWindowTitle('Piet Interpreter')
        self.setWindowIcon(QIcon('icon.png'))

        self.label = QLabel(self)
        qpm = QPixmap(self.image)
        qpm = qpm.scaled(800, 800, 1)

        self.label.setPixmap(qpm)
        self.label.setGeometry(50, 50, qpm.width(), qpm.height())

        button_run = QPushButton('Run', self)
        button_run.setCheckable(True)
        button_run.move(1500 - 100, 900 - 100)
        button_run.clicked[bool].connect(self.main)

        button_next = QPushButton('Next Step', self)
        button_next.setCheckable(True)
        button_next.move(1500 - 100, 900 - 100 + 50)
        button_next.clicked[bool].connect(self.main_trace)

        self.i = Interpreter(load_image(self.image))

        self.info1 = QLabel(self)
        self.info1.setText(str(self.i.stack))
        self.info1.setFont(QFont("Arial", 18))
        self.info1.setMinimumWidth(1000)
        self.info1.setVisible(True)
        self.info1.move(900, 100)

        self.info2 = QLabel(self)
        self.info2.setText("Function: ")
        self.info2.setFont(QFont("Arial", 18))
        self.info2.setMinimumWidth(500)
        self.info2.setMaximumWidth(500)
        self.info2.setVisible(True)
        self.info2.move(900, 50)

        self.info3 = QLabel(self)
        self.info3.setText("Output: ")
        self.info3.setFont(QFont("Arial", 18))
        self.info3.setMinimumWidth(500)
        self.info3.setMaximumWidth(500)
        self.info3.setVisible(True)
        self.info3.move(900, 150)

        self.dx = qpm.width() / (self.i.l - 2)
        self.star = QLabel(self)
        star = QPixmap('star.png')
        star = star.scaled(self.dx, self.dx)
        self.star.setPixmap(star)
        self.star.move(50 + (self.i.x - 1) * self.dx,
                       50 + (self.i.y - 1) * self.dx)
        self.show()

    def main(self):
        while True:
            if not self.i.start():
                break
            self.star.move(50 + (self.i.x - 1) * self.dx,
                           50 + (self.i.y - 1) * self.dx)
            self.info1.setText(str(self.i.stack))
            self.info2.setText("Function: " + self.i.command.__name__[1:])
            self.info3.setText("Output: " + self.i.out)

    def main_trace(self):
        self.i.start()
        self.star.move(50 + (self.i.x - 1) * self.dx,
                       50 + (self.i.y - 1) * self.dx)
        self.info1.setText(str(self.i.stack))
        self.info2.setText("Function: " + self.i.command.__name__[1:])
        self.info3.setText("Output: " + self.i.out)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == '--help':
            print('\nПример запуска программы: '
                  '`py piet_interp.py HelloWorld.png`')
            print('Пример запуска c режимом пошагового исполнения: '
                  '`py piet_interp.py HelloWorld.png --trace`')
        else:
            app = QApplication(sys.argv)
            ex = Example(sys.argv[1])
            sys.exit(app.exec_())
    else:
        print('\nСправка по запуску: `py piet_interp.py --help``')


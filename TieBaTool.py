from View.MainWindow import Example
from PyQt5.QtWidgets import *
import sys
sys.path.append("../")

app = QApplication(sys.argv)
ex = Example()
sys.exit(app.exec_())

raw_input()
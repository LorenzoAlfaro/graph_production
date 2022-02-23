import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()



if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    # End main UI code
    mw.show()
    sys.exit(app.exec())
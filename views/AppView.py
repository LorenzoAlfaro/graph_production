
from PyQt5 import QtWidgets as qtw

class AppView(qtw.QWidget):

    def __init__(self)-> None:
        qtw.QWidget.__init__(self)

        self.tabs = qtw.QTabWidget()

        self.layout = qtw.QFormLayout()
        self.layout.addRow(self.tabs)
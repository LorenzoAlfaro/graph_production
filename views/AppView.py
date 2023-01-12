
from PyQt5 import QtWidgets as qtw
from views.OptionsView import OptionsView

class AppView(qtw.QWidget):

    def __init__(self)-> None:
        qtw.QWidget.__init__(self)

        self.tabs = qtw.QTabWidget()

        self.OptionsView = OptionsView()
        self.tabs.addTab(self.OptionsView, "Plot Options")

        self.layout = qtw.QFormLayout()
        self.layout.addRow(self.tabs)
        self.setLayout(self.layout)
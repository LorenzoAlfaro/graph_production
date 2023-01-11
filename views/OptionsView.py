from PyQt5 import QtWidgets as qtw

class OptionsView(qtw.QWidget):

    def __init__(self) -> None:
        qtw.QWidget.__init__(self)
        self.layout = qtw.QFormLayout()

        self.drone_born_chkbox = qtw.QCheckBox()
        self.drone_born_chkbox.setCheckable(True)
        self.layout.addRow(qtw.QLabel("Plot Drone Born"), self.drone_born_chkbox)

        self.setLayout(self.layout)



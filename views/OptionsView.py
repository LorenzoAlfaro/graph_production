from PyQt5 import QtWidgets as qtw

class OptionsView(qtw.QWidget):

    def __init__(self) -> None:
        qtw.QWidget.__init__(self)
        self.layout = qtw.QFormLayout()

        self.drone_born_chkbox = qtw.QCheckBox()
        self.drone_born_chkbox.setCheckable(True)
        self.load_replay_bttn = qtw.QPushButton("Select Replay")
        self.plot_bttn = qtw.QPushButton("Plot Replay")
        self.player1_lbl = qtw.QLabel("Player 1 ?")
        self.player2_lbl = qtw.QLabel("Player 2 ?")
        self.layout.addRow(qtw.QLabel("Load Replay"), self.load_replay_bttn)
        self.layout.addRow(qtw.QLabel("Plot Replay"), self.plot_bttn)
        self.layout.addRow(qtw.QLabel("Plot Drone Born"), self.drone_born_chkbox)
        self.layout.addRow(qtw.QLabel("Player 1"), self.player1_lbl)
        self.layout.addRow(qtw.QLabel("Player 2"), self.player2_lbl)

        self.setLayout(self.layout)



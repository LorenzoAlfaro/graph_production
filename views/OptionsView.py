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
        self.unit_name_textbox = qtw.QLineEdit()
        self.players_combo_box = qtw.QComboBox(self)
        self.layout.addRow(qtw.QLabel("Load Replay"), self.load_replay_bttn)
        self.layout.addRow(qtw.QLabel("Plot Replay"), self.plot_bttn)
        self.layout.addRow(qtw.QLabel("Plot Drone Born"), self.drone_born_chkbox)
        self.layout.addRow(qtw.QLabel("Player 1"), self.player1_lbl)
        self.layout.addRow(qtw.QLabel("Player 2"), self.player2_lbl)
        self.layout.addRow(qtw.QLabel("Players"), self.players_combo_box)
        self.layout.addRow(qtw.QLabel("Unit"),self.unit_name_textbox)

        self.setLayout(self.layout)

    def populate_player(self, players_dict):
        self.players_combo_box.clear()
        for player in players_dict:
            self.players_combo_box.addItem(player)


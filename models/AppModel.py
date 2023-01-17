from PyQt5 import QtCore as qtc

class AppModel(qtc.QObject):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AppModel, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()

    replay_path = ""
    replay_path_signal = qtc.pyqtSignal(str)

    player_dict = {}
    player_dict_signal = qtc.pyqtSignal(object)

    def set_replay_path(self, path):
        self.replay_path = path
        self.replay_path_signal.emit(path)

    def set_players_dict(self, players):
        for player in players:
            self.player_dict[player.name] = player.uid
        self.player_dict_signal.emit(self.player_dict)
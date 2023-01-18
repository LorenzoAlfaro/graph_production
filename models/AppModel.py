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

    unit_name = "Drone"
    unit_name_signal = qtc.pyqtSignal(str)

    def set_replay_path(self, path):
        self.replay_path = path
        self.replay_path_signal.emit(path)

    def set_players_dict(self, players):
        for player in players:
            if not player.is_human :
                continue
            self.player_dict[player.name] = player.uid
        self.player_dict_signal.emit(self.player_dict)

    def set_unit_name(self, name:str):
        self.unit_name = name
        self.unit_name_signal.emit(name)
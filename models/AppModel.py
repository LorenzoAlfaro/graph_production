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

    def set_replay_path(self, path):
        self.replay_path = path
        self.replay_path_signal.emit(path)
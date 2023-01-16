
from PyQt5 import QtCore as qtc
from models.AppModel import AppModel
from PyQt5 import QtWidgets as qtw
from functions.stats import worker_timeline
import sc2reader as sc2

class Controller(qtc.QObject):

    def __init__(self, model: AppModel):
        super().__init__()
        self.model = model

    def select_replay(self, app):
        fname = qtw.QFileDialog.getOpenFileName(app, 'Open file',
                '/home/pi/Downloads/',"Replays(*.SC2Replay)")
        self.model.set_replay_path(fname[0])
        replay = sc2.load_replay(fname[0], load_map = False)
        worker_timeline(replay)
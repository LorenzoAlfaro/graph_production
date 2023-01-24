from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
import sc2reader as sc2
from models.AppModel import AppModel
from functions.stats import worker_timeline

class Controller(qtc.QObject):

    def __init__(self, model: AppModel):
        super().__init__()
        self.model = model
        self.folder = self.model.replay_folder
        self.replay = None

    def plot_graph(self):
        event_names = set([event.name for event in self.replay.events])
        print(event_names)
        worker_timeline(self.replay, unit_name = self.model.unit_name)

    def load_replay(self, app):
        fname = qtw.QFileDialog.getOpenFileName(app, 'Open file', self.folder, 'Replays(*.SC2Replay)')
        self.model.set_replay_path(fname[0])
        self.replay = sc2.load_replay(fname[0], load_map = False)

        self.model.player_dict.clear()
        self.model.set_players_dict(self.replay.players)

    def player_selected_changed(self, name):
        print(self.model.player_dict[name])
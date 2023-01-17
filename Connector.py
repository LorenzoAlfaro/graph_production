from controllers.Controller import Controller
from models.AppModel import AppModel
from views.AppView import AppView

def connectModel(AppView: AppView,Model: AppModel,Controller: Controller, UpdateSpinner):

    AppView.OptionsView.load_replay_bttn.clicked.connect(lambda: Controller.load_replay(AppView))
    AppView.OptionsView.plot_bttn.clicked.connect(lambda: Controller.plot_graph())
    Model.player_dict_signal.connect(AppView.OptionsView.populate_player)
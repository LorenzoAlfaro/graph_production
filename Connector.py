from controllers.Controller import Controller
from models.AppModel import AppModel
from views.AppView import AppView

def connectModel(AppView: AppView,Model: AppModel,Controller: Controller, UpdateSpinner):

    AppView.OptionsView.load_replay_bttn.clicked.connect(lambda: Controller.load_replay(AppView))
    AppView.OptionsView.plot_bttn.clicked.connect(lambda: Controller.plot_graph())
    AppView.OptionsView.unit_name_textbox.textChanged.connect(Model.set_unit_name)
    AppView.OptionsView.players_combo_box.currentTextChanged.connect(Model.set_player_1_selected)
    Model.player_dict_signal.connect(AppView.OptionsView.populate_player)
    Model.player_1_selected_signal.connect(lambda name: Controller.player_selected_changed(name))
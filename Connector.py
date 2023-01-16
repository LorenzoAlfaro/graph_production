from controllers.Controller import Controller
from models.AppModel import AppModel
from views.AppView import AppView

def connectModel(AppView: AppView,Model: AppModel,Controller: Controller, UpdateSpinner):

    AppView.OptionsView.open_replay_bttn.clicked.connect(lambda: Controller.select_replay(AppView))
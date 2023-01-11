
from PyQt5 import QtCore as qtc
from models.AppModel import AppModel

class Controller(qtc.QObject):

    def __init__(self, model: AppModel):
        super().__init__()
from PyQt5 import QtCore as qtc

class AppModel(qtc.QObject):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AppModel, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
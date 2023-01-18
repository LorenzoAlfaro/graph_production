import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import os.path, time
import mysql.connector
from decouple import config
from Connector import connectModel
from waitingspinnerwidget       import QtWaitingSpinner
from models.AppModel            import AppModel
from views.AppView import AppView
from controllers.Controller import Controller


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()

        self.version = ' 1.0'
        # self.setWindowIcon(qtg.QIcon('flask.png'))
        self.setGeometry(500, 100, 600, 640)
        self.setWindowTitle("StarCraft II Trainer" + self.version)

        self.Model                  = AppModel()
        self.Controller             = Controller(self.Model)
        self.AppView                = AppView()
        self.spinner                = QtWaitingSpinner(self)
        self.setCentralWidget(self.AppView)
        connectModel(self.AppView,self.Model,self.Controller,self.UpdateSpinner)

        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

        password = config('MYSQL_PASSWORD',default='')
        user = config('USER_NAME', default='')

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def _createToolBar(self):
        tools = qtw.QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def _createStatusBar(self):
        status = qtw.QStatusBar()
        status.showMessage("Ready")
        status.addWidget(self.spinner)
        self.setStatusBar(status)

    def UpdateSpinner(self, waiting):
        if waiting:
            self.spinner.start()
        else:
            self.spinner.stop()

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    # End main UI code
    mw.show()
    sys.exit(app.exec())
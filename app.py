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

    fileWatcher = qtc.QFileSystemWatcher()

    def __init__(self):
        super().__init__()

        self.version = ' 1.0'
        # self.setWindowIcon(qtg.QIcon('flask.png'))
        self.setGeometry(500, 100, 600, 640)
        self.setWindowTitle("SC2 Trainer" + self.version)

        self.Model                  = AppModel()
        self.Controller             = Controller(self.Model)
        self.AppView                = AppView()
        self.spinner                = QtWaitingSpinner(self)
        self.setCentralWidget(self.AppView)
        connectModel(self.AppView,self.Model,self.Controller,self.UpdateSpinner)

        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

        password = config('MYSQL_PASSWORD')
        user = config('USER_NAME')

        # self.fileWatcher.addPath("C:\\Users\\e420882\\Desktop\\TEST")
        # self.fileWatcher.directoryChanged.connect(lambda p:print('file has changed'+p) )
        # self.findNewFile()
        # keep track of the most recent file

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

    def findNewFile(self):
        print("Created: %s" % time.ctime(os.path.getctime("C:\\Users\\e420882\\Desktop\\TEST\\A.txt")))

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    # End main UI code
    mw.show()
    sys.exit(app.exec())
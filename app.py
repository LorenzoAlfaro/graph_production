import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import os.path, time


class MainWindow(qtw.QMainWindow):

    fileWatcher = qtc.QFileSystemWatcher()

    def __init__(self):
        super().__init__()

        self.fileWatcher.addPath("C:\\Users\\e420882\\Desktop\\TEST")

        self.fileWatcher.directoryChanged.connect(lambda p:print('file has changed'+p) )

        self.findNewFile()

        # keep track of the most recent file



    def findNewFile(self):

        print("Created: %s" % time.ctime(os.path.getctime("C:\\Users\\e420882\\Desktop\\TEST\\A.txt")))
        pass

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    # End main UI code
    mw.show()
    sys.exit(app.exec())
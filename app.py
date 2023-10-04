import sys
import os.path
import time
import logging
import shutil
from pathlib import Path

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import mysql.connector
from decouple import AutoConfig

from Connector import connectModel
from waitingspinnerwidget import QtWaitingSpinner
from models.AppModel import AppModel
from views.AppView import AppView
from controllers.Controller import Controller
from tufup.client import Client
import settings

logger = logging.getLogger(__name__)

__version__  = settings.APP_VERSION

is_frozen = False
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    bundle_dir = Path(sys._MEIPASS)
    path_exe = sys.executable
    is_frozen = True
else:
    bundle_dir = Path(__file__).parent
    path_exe = f'{sys.executable}\" \"{sys.argv[0]}'
path_to_dat = Path.cwd() / bundle_dir

config = AutoConfig(search_path=path_to_dat)

custom_template =  """@echo off
{log_lines}
echo Moving app files...
robocopy "{src_dir}" "{dst_dir}" {robocopy_options}
echo Done.
echo Restarting app
start "" "{app_exe_path}"
{delete_self}
"""
custom_template_variables = dict(
    app_exe_path=path_exe,
)

def progress_hook(bytes_downloaded: int, bytes_expected: int):
    progress_percent = bytes_downloaded / bytes_expected * 100
    print(f'\r{progress_percent:.1f}%', end='')
    # time.sleep(0.2)  # quick and dirty: simulate slow or large download
    if progress_percent >= 100:
        print('')


def update(pre: str):
    # Create update client
    client = Client(
        app_name=settings.APP_NAME,
        app_install_dir=settings.INSTALL_DIR,
        current_version=settings.APP_VERSION,
        metadata_dir=settings.METADATA_DIR,
        metadata_base_url=settings.METADATA_BASE_URL,
        target_dir=settings.TARGET_DIR,
        target_base_url=settings.TARGET_BASE_URL,
        refresh_required=False,
    )

    # Perform update
    if client.check_for_updates(pre=pre):
        client.download_and_apply_update(
            # WARNING: Be very careful with purge_dst_dir=True, because this
            # will delete *EVERYTHING* inside the app_install_dir, except
            # paths specified in exclude_from_purge. So, only use
            # purge_dst_dir=True if you are certain that your app_install_dir
            # does not contain any unrelated content.
            batch_template=custom_template,
            batch_template_extra_kwargs=custom_template_variables,
            progress_hook=progress_hook,
            purge_dst_dir=False,
            exclude_from_purge=None,
            log_file_name='install.log',
            skip_confirmation=True
        )
def main(cmd_args):
    # extract options from command line args
    pre_release_channel = cmd_args[0] if cmd_args else None  # 'a', 'b', or 'rc'

    # The app must ensure dirs exist
    for dir_path in [settings.INSTALL_DIR, settings.METADATA_DIR, settings.TARGET_DIR]:
        dir_path.mkdir(exist_ok=True, parents=True)

    # The app must be shipped with a trusted "root.json" metadata file,
    # which is created using the tufup.repo tools. The app must ensure
    # this file can be found in the specified metadata_dir. The root metadata
    # file lists all trusted keys and TUF roles.
    if not settings.TRUSTED_ROOT_DST.exists():
        shutil.copy(src=settings.TRUSTED_ROOT_SRC, dst=settings.TRUSTED_ROOT_DST)
        logger.info('Trusted root metadata copied to cache.')

    # Download and apply any available updates
    update(pre=pre_release_channel)

class MainWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()

        self.version = __version__
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
    main(sys.argv[1:])
    print('start GUI')
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    # End main UI code
    mw.show()
    sys.exit(app.exec())

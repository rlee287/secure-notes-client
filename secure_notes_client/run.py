import os
import sys

from PySide2 import QtWidgets

from gui_main import MainWindowClass
import thread_pool
from config_obj import ConfigObj
from ui.main_window import *

def setup_homedir(config):
    if not os.path.isdir(config.basedir):
        os.mkdir(config.basedir)

try:
    thread_pool.init_thread_pool()
    app = QtWidgets.QApplication(sys.argv)
    config=ConfigObj()
    setup_homedir(config)
    window_obj=MainWindowClass(Ui_MainWindow(), config)
    window_obj.show()
    exit_code=app.exec_()
    sys.exit(exit_code)
finally:
    thread_pool.deinit_thread_pool()
    config.__del__()

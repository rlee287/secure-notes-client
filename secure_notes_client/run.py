import sys
from PySide2 import QtWidgets

from gui import MainWindowClass
import thread_pool
from ui.main_window import *

def first_time_setup():
    pass

try:
    thread_pool.init_thread_pool()
    app = QtWidgets.QApplication(sys.argv)
    window_obj=MainWindowClass(Ui_MainWindow())
    window_obj.show()
    exit_code=app.exec_()
    sys.exit(exit_code)
finally:
    thread_pool.deinit_thread_pool()

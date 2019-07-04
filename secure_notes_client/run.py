import sys
from PySide2 import QtWidgets

from gui import MainWindowClass
from ui.main_window import *

def first_time_setup():
    pass

app = QtWidgets.QApplication(sys.argv)
window_obj=MainWindowClass(Ui_MainWindow())
window_obj.show()
exit_code=app.exec_()
sys.exit(exit_code)

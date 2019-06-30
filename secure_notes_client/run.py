import sys
import pprint

from PySide2 import QtWidgets
from ui.main_window import *
import login_gui

def set_up_ui():
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.actionLogin.triggered.connect(login_gui.create_login_dialog)
    return MainWindow

app = QtWidgets.QApplication(sys.argv)
window_obj=set_up_ui()
window_obj.show()
sys.exit(app.exec_())


from ui.login_dialog import *
from PySide2 import QtWidgets

def create_login_dialog():
    # UIC generated file does not inherit from QDialog
    # So set up the form and call exec_
    # in a slightly nonconventional manner
    dialog_form=QtWidgets.QDialog()
    dialog_ui_form=Ui_LoginDialog()
    dialog_ui_form.setupUi(dialog_form)
    # Use exec_() instead of open() as we want application blocking
    # Also open() does not display properly
    # (Environment=Kubuntu Linux 18.04, Qt 5.11.1)
    login_response_code=dialog_form.exec_()
    if login_response_code==QtWidgets.QDialog.Rejected:
        return
    print(dialog_ui_form.usernameLineEdit.text())
    print(dialog_ui_form.passwordLineEdit.text())

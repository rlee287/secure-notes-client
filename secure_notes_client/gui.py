from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QCoreApplication

from ui.login_dialog import *
from config_obj import ConfigObj
import networking

class MainWindowClass(QtWidgets.QMainWindow):
    logout_text="You are currently not logged in."
    login_text="You are logged in as {}."
    def __init__(self, ui_obj):
        super().__init__()
        self.ui_obj=ui_obj
        self.config_obj=ConfigObj()
        ui_obj.setupUi(self)
        ui_obj.actionLogin.triggered.connect(self.create_login_dialog)
        ui_obj.actionLogout.triggered.connect(self.create_logout_dialog)
        self.update_loginlabel_text()

    def update_loginlabel_text(self):
        current_username=self.config_obj.username
        if current_username: #Is not empty
            self.ui_obj.loginLabel.setText(
                    self.login_text.format(current_username))
            self.ui_obj.actionLogin.setEnabled(False)
            self.ui_obj.actionLogout.setEnabled(True)
        else:
            self.ui_obj.loginLabel.setText(self.logout_text)
            self.ui_obj.actionLogin.setEnabled(True)
            self.ui_obj.actionLogout.setEnabled(False)

    def create_login_dialog(self):
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
        username=dialog_ui_form.usernameLineEdit.text()
        password=dialog_ui_form.passwordLineEdit.text()
        self.ui_obj.actionLogin.setEnabled(False)
        self.ui_obj.actionLogout.setEnabled(False)
        progress_dialog=QtWidgets.QProgressDialog("Logging in...","Cancel",0,2,self)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setValue(0)
        QCoreApplication.processEvents()
        token=networking.get_login_token(self.config_obj.url,username,password)
        if token is None:
            progress_dialog.cancel()
            QtWidgets.QMessageBox.warning(self,
                    "Login Failed","Unable to log in.")
            self.update_loginlabel_text()
            return
        progress_dialog.setValue(1)
        self.config_obj.username=username
        self.config_obj.token=token
        progress_dialog.setValue(2)
        QtWidgets.QMessageBox.information(self,
                "Login successful","You have successfully logged in.")

        self.update_loginlabel_text()

    def create_logout_dialog(self):
        logout_confirm=QtWidgets.QMessageBox()
        logout_confirm.setText("Confirm logging out?")
        logout_confirm.setStandardButtons(QtWidgets.QMessageBox.Ok |
                QtWidgets.QMessageBox.Cancel)
        logout_ret_code=logout_confirm.exec_()
        # Dialog close is also caught here
        if logout_ret_code==QtWidgets.QMessageBox.Cancel:
            return
        # Only other option is OK here
        self.ui_obj.actionLogin.setEnabled(False)
        self.ui_obj.actionLogout.setEnabled(False)
        logout_status=networking.send_logout_request(self.config_obj.url,
                self.config_obj.token)
        if logout_status:
            QtWidgets.QMessageBox.information(self,
                    "Logout successful","You have successfully logged out.")
        else:
            QtWidgets.QMessageBox.warning(self,
                    "Logout Failed","Unable to log out.")
            return
        self.config_obj.username=""
        self.config_obj.token=""
        self.update_loginlabel_text()

    def closeEvent(self, event):
        # Proceed regardless of request status
        if self.config_obj.username:
            networking.send_logout_request(
                    self.config_obj.url,self.config_obj.token)
        event.accept()

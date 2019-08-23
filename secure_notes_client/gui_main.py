from PySide2 import QtWidgets
from PySide2.QtCore import Qt, Slot, QCoreApplication

from ui.login_dialog import Ui_LoginDialog
from ui.create_dialog import Ui_NoteCreationDialog
from ui.note_edit_window import Ui_NoteEditWindow
from gui_editor import EditorClass

import filesystem
import networking

class MainWindowClass(QtWidgets.QMainWindow):
    logout_text="You are currently not logged in."
    login_text="You are logged in as {}."
    
    def __init__(self, ui_obj, config_obj):
        super().__init__()
        self.ui_obj=ui_obj
        self.config_obj=config_obj
        self.list_subwindow=list()
        ui_obj.setupUi(self)
        ui_obj.actionLogin.triggered.connect(self.login_action)
        ui_obj.actionLogout.triggered.connect(self.logout_action)
        
        ui_obj.actionCreate.triggered.connect(self.create_action)
        ui_obj.actionRefresh.triggered.connect(self.refresh_note_list_dialog)
        
        ui_obj.noteTreeWidget.itemDoubleClicked.connect(self.print_clicked_item)
        self.update_loginlabel_text()

    @Slot(QtWidgets.QTreeWidgetItem, int)
    def print_clicked_item(self, item, column):
        print([item.text(i) for i in range(item.columnCount())])
        note_window = EditorClass(Ui_NoteEditWindow(),
                                   self.config_obj,
                                   item.text(item.columnCount()-1))
        note_window.show()
        self.list_subwindow.append(note_window)
        print(self.list_subwindow)

    def update_loginlabel_text(self):
        current_username=self.config_obj.username
        if current_username: #Is not empty
            self.ui_obj.loginLabel.setText(
                    self.login_text.format(current_username))
            self.ui_obj.actionLogin.setEnabled(False)
            self.ui_obj.actionLogout.setEnabled(True)

            self.ui_obj.actionCreate.setEnabled(True)
            self.ui_obj.actionSearch.setEnabled(True)
            self.ui_obj.actionRefresh.setEnabled(True)
        else:
            self.ui_obj.loginLabel.setText(self.logout_text)
            self.ui_obj.actionLogin.setEnabled(True)
            self.ui_obj.actionLogout.setEnabled(False)
            self.ui_obj.actionCreate.setEnabled(False)
            self.ui_obj.actionSearch.setEnabled(False)
            self.ui_obj.actionRefresh.setEnabled(False)

    def login_action(self):
        login_ui_form=Ui_LoginDialog()
        _,login_response_code=MainWindowClass.spawn_uic_dialog_modal(login_ui_form)
        if login_response_code==QtWidgets.QDialog.Rejected:
            return
        username=login_ui_form.usernameLineEdit.text()
        password=login_ui_form.passwordLineEdit.text()
        self.ui_obj.actionLogin.setEnabled(False)
        self.ui_obj.actionLogout.setEnabled(False)

        progress_dialog=QtWidgets.QProgressDialog("Logging in...","",0,3,self)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setValue(0)
        QCoreApplication.processEvents()
        token=networking.get_login_token(self.config_obj.url,(username,password))
        #TODO: differentiate between bad login and unavailable server
        if token is None:
            progress_dialog.cancel()
            QtWidgets.QMessageBox.warning(self,
                    "Login Failed","Unable to log in.")
            self.update_loginlabel_text()
            return

        progress_dialog.setValue(1)
        self.config_obj.username=username
        self.config_obj.token=token
        filesystem.populate_userdir(self.config_obj,password)
        self.config_obj.update_key(password)
        progress_dialog.setValue(2)
        self.refresh_note_list()
        progress_dialog.setValue(3)

        self.update_loginlabel_text()
        QtWidgets.QMessageBox.information(self,
                "Login successful","You have successfully logged in.")

    def logout_action(self):
        logout_confirm=QtWidgets.QMessageBox()
        logout_confirm.setText("Confirm logging out as {}?"
                               .format(self.config_obj.username))
        logout_confirm.setStandardButtons(QtWidgets.QMessageBox.Ok |
                QtWidgets.QMessageBox.Cancel)
        logout_ret_code=logout_confirm.exec_()
        # Dialog close is also caught here
        if logout_ret_code==QtWidgets.QMessageBox.Cancel:
            return
        # Only other option is OK here
        self.ui_obj.actionLogin.setEnabled(False)
        self.ui_obj.actionLogout.setEnabled(False)
        logout_status=networking.send_logout_request(self.config_obj)
        if logout_status:
            # Changing username also invalidates token and key
            self.config_obj.username=""
            self.ui_obj.noteTreeWidget.clear()
            self.update_loginlabel_text()
            QtWidgets.QMessageBox.information(self,
                    "Logout successful","You have successfully logged out.")
        else:
            QtWidgets.QMessageBox.warning(self,
                    "Logout Failed","Unable to log out.")
            return

    def refresh_note_list(self):
        list_notes=networking.get_list(self.config_obj)
        if list_notes is None:
            return False
        self.ui_obj.noteTreeWidget.clear()
        for note_id in list_notes:
            note_req=networking.get_note(self.config_obj,note_id)
            filesystem.write_noteobj(self.config_obj,note_req)
            note_item=QtWidgets.QTreeWidgetItem([note_req["note"]["title"],
                                                 note_req["Last-Modified"],
                                                 note_req["note"]["text"][:50],
                                                 note_req["note"]["_id"]])
            self.ui_obj.noteTreeWidget.addTopLevelItem(note_item)
        return True
    
    def refresh_note_list_dialog(self):
        if not self.refresh_note_list():
            QtWidgets.QMessageBox.warning(self,
                    "Note Refresh Failed","Unable to refresh list of notes.")
    
    def create_action(self):
        create_ui_form=Ui_NoteCreationDialog()
        _,create_response_code=self.spawn_uic_dialog_modal(create_ui_form)
        if create_response_code==QtWidgets.QDialog.Rejected:
            return
        new_title=create_ui_form.titleLineEdit.text()
        print(new_title)
        print(create_ui_form.radioPlain.isChecked())
        print(create_ui_form.radioCompressed.isChecked())
        note_make=networking.make_note(self.config_obj,
                                       new_title,"plain")
        note_item=QtWidgets.QTreeWidgetItem([new_title,
                                            note_make["Last-Modified"],
                                            ""])
        self.ui_obj.noteTreeWidget.addTopLevelItem(note_item)

    @staticmethod
    def spawn_uic_dialog_modal(dialog_ui_form):
        # UIC generated file does not inherit from QDialog
        # So set up the form and call exec_
        # in a slightly nonconventional manner
        dialog_form=QtWidgets.QDialog()
        dialog_ui_form.setupUi(dialog_form)
        # Use exec_() instead of open() as we want application blocking
        # Also open() does not display properly
        # (Environment=Kubuntu Linux 18.04, Qt 5.11.1)
        # Return both the QDialog object and the return code for GC purposes
        return dialog_form,dialog_form.exec_()

    def closeEvent(self, event):
        # Proceed regardless of request status
        if self.config_obj.username:
            networking.send_logout_request(self.config_obj)
        event.accept()

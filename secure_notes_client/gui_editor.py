from PySide2 import QtWidgets
from PySide2.QtCore import Signal, Qt

import filesystem
import networking

class EditorClass(QtWidgets.QMainWindow):
    close_signal = Signal(QtWidgets.QMainWindow)
    
    def __init__(self, ui_obj, config_obj, note_id):
        # type: (EditorClass, Ui_NoteEditWindow, ConfigObj, str) -> None
        super().__init__()

        self.ui_obj = ui_obj
        self.config_obj = config_obj
        self.note_id = note_id
        self.edited_since_last_save = False
        self.allow_edits = False
        self.note_obj=filesystem.read_noteobj(config_obj,note_id)

        ui_obj.setupUi(self)

        self.setAttribute(Qt.WA_DeleteOnClose,True)
        self.setWindowTitle(self.note_obj["note"]["title"])
        ui_obj.titleLineEdit.setText(self.note_obj["note"]["title"])
        ui_obj.noteTextEdit.setPlainText(self.note_obj["note"]["text"])

        ui_obj.titleLineEdit.editingFinished.connect(self.mark_edited)
        ui_obj.noteTextEdit.textChanged.connect(self.mark_edited)
        ui_obj.actionSave.triggered.connect(self.save_file)

        self.update_editor_enabled_status()
    
    def set_editing_enabled(self, enable_editing):
        if self.allow_edits == enable_editing:
            return
        if self.allow_edits: # T -> F, throw warning if unsaved changes
            if self.edited_since_last_save:
                raise ValueError("Unsaved changes present")
        else: # F -> T, just do enabling
            self.allow_edits = True
            self.edited_since_last_save = False
        self.update_editor_enabled_status()
    
    def update_editor_enabled_status(self):
        self.ui_obj.titleLineEdit.setReadOnly(not self.allow_edits)
        self.ui_obj.noteTextEdit.setReadOnly(not self.allow_edits)

    def mark_edited(self):
        self.edited_since_last_save = True
    
    def save_file(self):
        note_obj_copy = self.note_obj.copy()
        note_obj_copy["note"]["title"] = ui_obj.titleLineEdit.getText()
        note_obj_copy["note"]["text"] = ui_obj.noteTextEdit.getText()
        self.edited_since_last_save = False

    def closeEvent(self, event):
        # TODO: confirmation dialog stuff
        self.close_signal.emit(self)
        event.accept()
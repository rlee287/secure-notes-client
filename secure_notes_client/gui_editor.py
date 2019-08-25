from PySide2 import QtWidgets

import filesystem
import networking

class EditorClass(QtWidgets.QMainWindow):
    def __init__(self, ui_obj, config_obj, note_id):
        # type: (EditorClass, Ui_NoteEditWindow, ConfigObj, str) -> None
        super().__init__()
        self.ui_obj = ui_obj
        self.config_obj = config_obj
        self.note_id = note_id
        self.edited_since_last_save = False
        self.note_obj=filesystem.read_noteobj(config_obj,note_id)

        ui_obj.setupUi(self)

        self.setWindowTitle(self.note_obj["note"]["title"])
        ui_obj.titleLineEdit.setText(self.note_obj["note"]["title"])
        ui_obj.noteTextEdit.setPlainText(self.note_obj["note"]["text"])

        ui_obj.titleLineEdit.editingFinished.connect(self.mark_edited)
        ui_obj.noteTextEdit.textChanged.connect(self.mark_edited)
        ui_obj.actionSave.triggered.connect(self.save_file)

    def mark_edited(self):
        self.edited_since_last_save = True
    
    def save_file(self):
        note_obj_copy = self.note_obj.copy()
        note_obj_copy["note"]["title"] = ui_obj.titleLineEdit.getText()
        note_obj_copy["note"]["text"] = ui_obj.noteTextEdit.getText()
        self.edited_since_last_save = False
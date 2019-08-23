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
        ui_obj.setupUi(self)
        note_obj=filesystem.read_noteobj(config_obj,note_id)
        self.setWindowTitle(note_obj["note"]["title"])
        ui_obj.noteTextEdit.setPlainText(note_obj["note"]["text"])

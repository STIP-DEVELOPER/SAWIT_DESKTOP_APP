from PyQt5.QtCore import QObject, pyqtSignal


class AppState(QObject):
    value_changed = pyqtSignal(str, object)

    def __init__(self):
        super().__init__()
        self.settings = {
            "model_path": "models/best.pt",
            "camera_index": 0,
            "confidence": 0.5,
        }

    def update(self, key, value):
        self.settings[key] = value
        self.value_changed.emit(key, value)

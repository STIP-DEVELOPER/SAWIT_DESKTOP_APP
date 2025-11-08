from PyQt5.QtCore import QObject, pyqtSignal


class AppState(QObject):
    """Global state untuk menyimpan data yang digunakan di berbagai screen."""

    setting_changed = pyqtSignal(str, object)

    def __init__(self):
        super().__init__()
        self._settings = {}

    def set_value(self, key, value):
        """Ubah nilai dan kirim sinyal ke listener lain."""
        self._settings[key] = value
        self.setting_changed.emit(key, value)

    def get_value(self, key, default=None):
        """Ambil nilai dari state global."""
        return self._settings.get(key, default)


app_state = AppState()

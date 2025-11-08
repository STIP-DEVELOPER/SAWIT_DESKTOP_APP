from .app_state import app_state


def set_setting(key, value):
    """Simpan nilai ke global state."""
    app_state.set_value(key, value)


def get_setting(key, default=None):
    """Ambil nilai dari global state."""
    return app_state.get_value(key, default)


def connect_to_state_change(slot_func):
    """Hubungkan fungsi ke sinyal perubahan state."""
    app_state.setting_changed.connect(slot_func)

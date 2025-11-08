from PyQt5.QtGui import QIcon
import os


def get_icon(name: str) -> QIcon:
    icon_path = os.path.join(os.getcwd(), "assets", "icons", name)
    return QIcon(icon_path) if os.path.exists(icon_path) else QIcon()

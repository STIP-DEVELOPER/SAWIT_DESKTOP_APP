from PyQt5.QtWidgets import QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from helpers.icon import get_icon


class HeaderMenu(QHBoxLayout):
    page_changed = pyqtSignal(str)
    exit_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_buttons = {}
        self._build_menu()

    def _build_menu(self):
        self.setSpacing(15)
        self.setContentsMargins(10, 10, 10, 10)

        menu_items = [
            ("home", "Home", "home.png"),
            ("logs", "Logs", "logs.png"),
            ("settings", "Settings", "settings.png"),
        ]

        for key, label, icon_file in menu_items:
            btn = QPushButton(f" {label}")
            btn.setIcon(get_icon(icon_file))
            btn.setCheckable(True)
            btn.setStyleSheet(self._menu_button_style())
            btn.clicked.connect(lambda checked, k=key: self.page_changed.emit(k))
            self.menu_buttons[key] = btn
            self.addWidget(btn)

        self.addStretch()

        # Exit Button
        exit_button = QPushButton(" Exit")
        exit_button.setIcon(get_icon("power.png"))
        exit_button.setStyleSheet(self._exit_button_style())
        exit_button.clicked.connect(self.exit_clicked.emit)
        self.addWidget(exit_button)

    def highlight(self, key: str):
        """Update checked state when page changes"""
        for k, btn in self.menu_buttons.items():
            btn.setChecked(k == key)

    def _menu_button_style(self):
        return """
        QPushButton {
            background-color: #1a1a1a;
            color: white;
            border-radius: 6px;
            padding: 8px 20px;
            font-size: 14px;
        }
        QPushButton:hover { background-color: #333; }
        QPushButton:checked {
            background-color: #00aaff;
            color: black;
            font-weight: bold;
        }
        """

    def _exit_button_style(self):
        return """
        QPushButton {
            background-color: #f52c80;
            color: white;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 14px;
        }
        QPushButton:hover { background-color: #d32f2f; }
        QPushButton:pressed { background-color: #880e4f; }
        """

import os
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QMessageBox,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from ui.pages.home import HomePage
from ui.pages.logs import LogsPage
from ui.pages.settings import SettingsPage


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Tractor UI")
        self.resize(1280, 720)
        self.show_camera = True

        self._build_ui()

        # === tampilkan fullscreen saat pertama kali dibuka ===
        self.showFullScreen()

    # -------------------------
    # ICON HELPER
    # -------------------------
    def _icon(self, name: str) -> QIcon:
        icon_path = os.path.join(os.getcwd(), "assets", "icons", name)
        return QIcon(icon_path) if os.path.exists(icon_path) else QIcon()

    # -------------------------
    # BUILD UI
    # -------------------------
    def _build_ui(self):
        # ===== MENU BAR =====
        self.menu_buttons = {}
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(15)
        menu_layout.setContentsMargins(10, 10, 10, 10)

        menu_items = [
            ("home", "Home", "home.png"),
            ("logs", "Logs", "logs.png"),
            ("settings", "Settings", "settings.png"),
        ]

        for key, label, icon_file in menu_items:
            btn = QPushButton(f" {label}")
            btn.setIcon(self._icon(icon_file))
            btn.setCheckable(True)
            btn.setStyleSheet(
                """
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
            )
            btn.clicked.connect(lambda checked, k=key: self._switch_page(k))
            self.menu_buttons[key] = btn
            menu_layout.addWidget(btn)

        menu_layout.addStretch()

        # ===== EXIT BUTTON (Header kanan) =====
        self.exit_button = QPushButton(" Exit")
        self.exit_button.setIcon(self._icon("power.png"))
        self.exit_button.setStyleSheet(
            """
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
        )
        self.exit_button.clicked.connect(self._confirm_exit)
        menu_layout.addWidget(self.exit_button)

        # ===== STACK AREA =====
        self.main_stack = QStackedWidget()
        self.page_home = HomePage()
        self.page_logs = LogsPage()
        self.page_settings = SettingsPage()

        self.main_stack.addWidget(self.page_home)
        self.main_stack.addWidget(self.page_logs)
        self.main_stack.addWidget(self.page_settings)

        # ===== MAIN LAYOUT =====
        main_layout = QVBoxLayout()
        main_layout.addLayout(menu_layout)
        main_layout.addWidget(self.main_stack)
        main_layout.setStretch(1, 1)
        self.setLayout(main_layout)

        self._switch_page("home")

        self.start_button = self.page_home.start_button
        self.stop_button = self.page_home.stop_button
        self.toggle_camera_button = self.page_home.toggle_camera_button
        self.camera_label = self.page_home.camera_label
        self.log_box = self.page_home.log_box

    # -------------------------
    # MENU SWITCH HANDLER
    # -------------------------
    def _switch_page(self, key: str):
        """Handle switching between stacked pages"""
        for k, btn in self.menu_buttons.items():
            btn.setChecked(k == key)

        if key == "home":
            self.main_stack.setCurrentWidget(self.page_home)
        elif key == "logs":
            self.main_stack.setCurrentWidget(self.page_logs)
            self.page_logs.load_logs()
        elif key == "settings":
            self.main_stack.setCurrentWidget(self.page_settings)

    # -------------------------
    # EXIT CONFIRMATION
    # -------------------------
    def _confirm_exit(self):
        reply = QMessageBox.question(
            self,
            "Exit Confirmation",
            "Are you sure you want to exit the application?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self.close()

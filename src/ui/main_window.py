from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QMessageBox,
)

from helpers.icon import get_icon
from ui.pages.home.page import HomePage
from ui.pages.logs.page import LogsPage
from ui.pages.settings.page import SettingsPage
from ui.styles.index import StyleShared


class MainWindow(QWidget):
    styles = StyleShared()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Tractor UI")
        self.resize(1280, 720)
        self.show_camera = True
        self._build_ui()
        self.showFullScreen()

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
            btn.setIcon(get_icon(icon_file))
            btn.setCheckable(True)
            btn.setStyleSheet(self.styles.menu_button())
            btn.clicked.connect(lambda checked, k=key: self._switch_page(k))
            self.menu_buttons[key] = btn
            menu_layout.addWidget(btn)

        menu_layout.addStretch()

        # ===== EXIT BUTTON (Header kanan) =====
        self.exit_button = QPushButton(" Exit")
        self.exit_button.setIcon(get_icon("power.png"))
        self.exit_button.setStyleSheet(self.styles.exit_button())
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

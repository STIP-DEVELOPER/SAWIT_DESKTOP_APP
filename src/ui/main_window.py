import json
import os
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QStackedWidget,
    QFileDialog,
    QLineEdit,
    QFormLayout,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from configs import config


class MainWindow(QWidget):
    CONFIG_FILE = os.path.join(os.getcwd(), "model_config.json")
    LOG_FILE = os.path.join(os.getcwd(), "logs.json")
    SETTINGS_FILE = os.path.join(os.getcwd(), "settings.json")

    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.WINDOW_TITLE)
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.show_camera = True

        self._build_ui()
        self._load_settings()
        self._load_last_model_selection()

    # ======================
    # ICON HELPER
    # ======================
    def _icon(self, name: str) -> QIcon:
        icon_path = os.path.join(os.getcwd(), "assets", "icons", name)
        return QIcon(icon_path) if os.path.exists(icon_path) else QIcon()

    # ======================
    # BUILD UI
    # ======================
    def _build_ui(self):
        # ===== MENU BAR (TOP) =====
        self.menu_buttons = {}
        menu_names = [
            ("home", "Home", "home.png"),
            ("logs", "Logs", "logs.png"),
            ("settings", "Settings", "settings.png"),
        ]
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(20)
        menu_layout.setContentsMargins(10, 10, 10, 10)

        for key, label, icon_name in menu_names:
            btn = QPushButton(f" {label}")
            btn.setIcon(self._icon(icon_name))
            btn.setCheckable(True)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #1a1a1a;
                    color: white;
                    border-radius: 6px;
                    padding: 10px 20px;
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
            btn.clicked.connect(lambda checked, k=key: self._on_menu_clicked(k))
            self.menu_buttons[key] = btn
            menu_layout.addWidget(btn)

        menu_layout.addStretch()

        # ===== MAIN STACK AREA =====
        self.main_stack = QStackedWidget()

        # --- HOME PAGE ---
        self.page_home = QWidget()
        home_layout = QVBoxLayout()

        self.camera_label = QLabel("Camera View")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setSizePolicy(
            self.camera_label.sizePolicy().Expanding,
            self.camera_label.sizePolicy().Expanding,
        )
        self.camera_label.setStyleSheet(
            """
            border: 2px solid #444;
            background-color: #111;
            color: #aaa;
            font-size: 14px;
        """
        )

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet(
            """
            background-color: #000;
            color: #0f0;
            font-family: Consolas, monospace;
            font-size: 13px;
        """
        )

        self.start_button = QPushButton("▶ Start")
        self.stop_button = QPushButton("⏹ Stop")
        self.toggle_camera_button = QPushButton("👁 Show/Hide Camera")
        self.exit_button = QPushButton("⏻ Exit")

        button_style = """
            QPushButton {
                background-color: #333;
                color: white;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #555; }
            QPushButton:pressed { background-color: #222; }
        """
        for btn in [
            self.start_button,
            self.stop_button,
            self.toggle_camera_button,
            self.exit_button,
        ]:
            btn.setStyleSheet(button_style)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.toggle_camera_button)
        control_layout.addWidget(self.exit_button)

        home_layout.addWidget(self.camera_label)
        home_layout.addWidget(self.log_box)
        home_layout.addLayout(control_layout)
        home_layout.setStretch(0, 3)
        home_layout.setStretch(1, 1)
        self.page_home.setLayout(home_layout)

        # --- LOGS PAGE ---
        self.page_logs = QWidget()
        logs_layout = QVBoxLayout()
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setStyleSheet(
            """
            background-color: #111;
            color: #0f0;
            border: 1px solid #333;
            font-family: Consolas, monospace;
            font-size: 13px;
        """
        )
        self.load_logs_button = QPushButton("🔄 Reload Logs")
        self.export_logs_button = QPushButton("💾 Export Logs")
        for btn in [self.load_logs_button, self.export_logs_button]:
            btn.setStyleSheet(button_style)
        self.load_logs_button.clicked.connect(self.load_logs)
        self.export_logs_button.clicked.connect(self.export_logs)

        logs_layout.addWidget(QLabel("📜 System Logs:"))
        logs_layout.addWidget(self.logs_text)
        logs_layout.addWidget(self.load_logs_button)
        logs_layout.addWidget(self.export_logs_button)
        logs_layout.addStretch()
        self.page_logs.setLayout(logs_layout)

        # --- SETTINGS PAGE ---
        self.page_settings = QWidget()
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.yolo_model_input = QLineEdit()
        self.camera_index_input = QLineEdit("0")
        self.yolo_img_size_input = QLineEdit("320")
        self.yolo_conf_input = QLineEdit("0.4")
        self.yolo_frame_skip_input = QLineEdit("5")
        self.serial_port_input = QLineEdit("/dev/tty.usbserial-1410")
        self.serial_baud_input = QLineEdit("9600")

        form_layout.addRow("YOLO Model:", self.yolo_model_input)
        form_layout.addRow("Camera Index:", self.camera_index_input)
        form_layout.addRow("YOLO Image Size:", self.yolo_img_size_input)
        form_layout.addRow("YOLO Confidence:", self.yolo_conf_input)
        form_layout.addRow("YOLO Frame Skip:", self.yolo_frame_skip_input)
        form_layout.addRow("Serial Port:", self.serial_port_input)
        form_layout.addRow("Serial Baudrate:", self.serial_baud_input)

        self.save_settings_button = QPushButton("💾 Save Settings")
        self.save_settings_button.setStyleSheet(button_style)
        self.save_settings_button.clicked.connect(self.save_settings)

        settings_layout = QVBoxLayout()
        settings_layout.addLayout(form_layout)
        settings_layout.addWidget(self.save_settings_button)
        settings_layout.addStretch()
        self.page_settings.setLayout(settings_layout)

        # Add all pages
        self.main_stack.addWidget(self.page_home)
        self.main_stack.addWidget(self.page_logs)
        self.main_stack.addWidget(self.page_settings)

        # ===== MAIN LAYOUT =====
        main_layout = QVBoxLayout()
        main_layout.addLayout(menu_layout)
        main_layout.addWidget(self.main_stack)
        main_layout.setStretch(1, 1)
        self.setLayout(main_layout)

        # Default to Home
        self._on_menu_clicked("home")

    # ======================
    # MENU HANDLER
    # ======================
    def _on_menu_clicked(self, key):
        for k, btn in self.menu_buttons.items():
            btn.setChecked(k == key)

        if key == "home":
            self.main_stack.setCurrentIndex(0)
        elif key == "logs":
            self.main_stack.setCurrentIndex(1)
            self.load_logs()
        elif key == "settings":
            self.main_stack.setCurrentIndex(2)

    # ======================
    # LOGS MANAGEMENT
    # ======================
    def load_logs(self):
        self.logs_text.clear()
        if os.path.exists(self.LOG_FILE):
            try:
                with open(self.LOG_FILE, "r") as f:
                    logs = json.load(f)
                    self.logs_text.setPlainText(json.dumps(logs, indent=4))
            except Exception as e:
                self.logs_text.setPlainText(f"Error reading log: {e}")
        else:
            self.logs_text.setPlainText("No log file found.")

    def export_logs(self):
        if not os.path.exists(self.LOG_FILE):
            self.logs_text.append("No logs to export.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Logs", "logs_export.json", "JSON Files (*.json)"
        )
        if path:
            try:
                with open(self.LOG_FILE, "r") as src, open(path, "w") as dst:
                    dst.write(src.read())
                self.logs_text.append(f"✅ Logs exported to {path}")
            except Exception as e:
                self.logs_text.append(f"❌ Failed to export logs: {e}")

    # ======================
    # SETTINGS MANAGEMENT
    # ======================
    def _load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r") as f:
                    settings = json.load(f)
                    self.yolo_model_input.setText(settings.get("YOLO_MODEL", ""))
                    self.camera_index_input.setText(
                        str(settings.get("CAMERA_INDEX", 0))
                    )
                    self.yolo_img_size_input.setText(
                        str(settings.get("YOLO_IMAGE_SIZE", 320))
                    )
                    self.yolo_conf_input.setText(
                        str(settings.get("YOLO_CONFIDENCE", 0.4))
                    )
                    self.yolo_frame_skip_input.setText(
                        str(settings.get("YOLO_FRAME_SKIP", 5))
                    )
                    self.serial_port_input.setText(
                        settings.get("SERIAL_PORT", "/dev/tty.usbserial-1410")
                    )
                    self.serial_baud_input.setText(
                        str(settings.get("SERIAL_BAUDRATE", 9600))
                    )
            except Exception as e:
                print(f"[WARN] Failed to load settings: {e}")

    def save_settings(self):
        data = {
            "YOLO_MODEL": self.yolo_model_input.text(),
            "CAMERA_INDEX": int(self.camera_index_input.text()),
            "YOLO_IMAGE_SIZE": int(self.yolo_img_size_input.text()),
            "YOLO_CONFIDENCE": float(self.yolo_conf_input.text()),
            "YOLO_FRAME_SKIP": int(self.yolo_frame_skip_input.text()),
            "SERIAL_PORT": self.serial_port_input.text(),
            "SERIAL_BAUDRATE": int(self.serial_baud_input.text()),
        }
        try:
            with open(self.SETTINGS_FILE, "w") as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Success", "✅ Settings saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ Failed to save settings: {e}")

    # ======================
    # MODEL CONFIG SAVE / LOAD
    # ======================
    def _load_last_model_selection(self):
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r") as f:
                    json.load(f)
            except Exception:
                pass

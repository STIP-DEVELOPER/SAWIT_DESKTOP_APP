import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
)


class SettingsPage(QWidget):
    def __init__(self, settings_file):
        super().__init__()
        self.settings_file = settings_file
        self._build_ui()
        self._load_settings()

    def _build_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)

        self.yolo_model = QLineEdit()
        self.camera_index = QLineEdit("0")
        self.img_size = QLineEdit("320")
        self.conf = QLineEdit("0.4")
        self.frame_skip = QLineEdit("5")
        self.serial_port = QLineEdit("/dev/ttyUSB0")
        self.serial_baud = QLineEdit("9600")

        form.addRow("YOLO Model:", self.yolo_model)
        form.addRow("Camera Index:", self.camera_index)
        form.addRow("Image Size:", self.img_size)
        form.addRow("Confidence:", self.conf)
        form.addRow("Frame Skip:", self.frame_skip)
        form.addRow("Serial Port:", self.serial_port)
        form.addRow("Baudrate:", self.serial_baud)

        self.save_button = QPushButton("💾 Save Settings")
        self.save_button.setStyleSheet(self._button_style())
        self.save_button.clicked.connect(self._save_settings)

        layout.addLayout(form)
        layout.addWidget(self.save_button)
        layout.addStretch()
        self.setLayout(layout)

    def _load_settings(self):
        if not os.path.exists(self.settings_file):
            return
        try:
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
                self.yolo_model.setText(settings.get("YOLO_MODEL", ""))
                self.camera_index.setText(str(settings.get("CAMERA_INDEX", 0)))
                self.img_size.setText(str(settings.get("YOLO_IMAGE_SIZE", 320)))
                self.conf.setText(str(settings.get("YOLO_CONFIDENCE", 0.4)))
                self.frame_skip.setText(str(settings.get("YOLO_FRAME_SKIP", 5)))
                self.serial_port.setText(settings.get("SERIAL_PORT", "/dev/ttyUSB0"))
                self.serial_baud.setText(str(settings.get("SERIAL_BAUDRATE", 9600)))
        except Exception as e:
            print(f"[WARN] Failed to load settings: {e}")

    def _save_settings(self):
        data = {
            "YOLO_MODEL": self.yolo_model.text(),
            "CAMERA_INDEX": int(self.camera_index.text()),
            "YOLO_IMAGE_SIZE": int(self.img_size.text()),
            "YOLO_CONFIDENCE": float(self.conf.text()),
            "YOLO_FRAME_SKIP": int(self.frame_skip.text()),
            "SERIAL_PORT": self.serial_port.text(),
            "SERIAL_BAUDRATE": int(self.serial_baud.text()),
        }
        try:
            with open(self.settings_file, "w") as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Success", "✅ Settings saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ Failed to save settings: {e}")

    def _button_style(self):
        return """
            QPushButton {
                background-color: #333;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #555; }
            QPushButton:pressed { background-color: #222; }
        """

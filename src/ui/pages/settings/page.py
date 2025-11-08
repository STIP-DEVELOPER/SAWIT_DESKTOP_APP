import json
import os
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QLabel,
    QSizePolicy,
    QHBoxLayout,
    QComboBox,
)

from core.logger import add_log
from enums.log import LogLevel, LogSource
from helpers.icon import get_icon
from ui.pages.settings.styles import SettingPageStyle


class SettingsPage(QWidget):
    styles = SettingPageStyle()

    def __init__(self):
        super().__init__()
        self.settings_file = "settings.json"
        self.models_path = os.path.join(os.getcwd(), "models")
        self._build_ui()
        self._load_settings()

    def _build_ui(self):
        layout = QVBoxLayout()

        # ======================
        # GRID FORM (2 kolom)
        # ======================
        grid = QGridLayout()
        grid.setSpacing(15)
        grid.setContentsMargins(20, 20, 20, 20)
        label_style = "color: #ccc; font-size: 14px;"

        # ======================
        # Input fields
        # ======================
        self.yolo_model = QComboBox()
        self.yolo_model.addItems(["small-tree", "medium-tree", "large-tree"])
        self.yolo_model.setStyleSheet(self.styles.model_layout())
        self.yolo_model.setMinimumHeight(40)
        self.yolo_model.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.camera_index = QLineEdit("0")
        self.img_size = QLineEdit("320")
        self.conf = QLineEdit("0.4")
        self.frame_skip = QLineEdit("5")
        self.serial_port = QLineEdit("/dev/ttyUSB0")
        self.serial_baud = QLineEdit("9600")

        for field in [
            self.camera_index,
            self.img_size,
            self.conf,
            self.frame_skip,
            self.serial_port,
            self.serial_baud,
        ]:
            field.setMinimumHeight(40)
            field.setStyleSheet(self.styles.input_field())
            field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        grid.addWidget(QLabel("YOLO Model:"), 0, 0, alignment=Qt.AlignRight)
        grid.addWidget(self.yolo_model, 0, 1)

        grid.addWidget(QLabel("Camera Index:"), 0, 2, alignment=Qt.AlignRight)
        grid.addWidget(self.camera_index, 0, 3)

        grid.addWidget(QLabel("Image Size:"), 1, 0, alignment=Qt.AlignRight)
        grid.addWidget(self.img_size, 1, 1)

        grid.addWidget(QLabel("Confidence:"), 1, 2, alignment=Qt.AlignRight)
        grid.addWidget(self.conf, 1, 3)

        grid.addWidget(QLabel("Frame Skip:"), 2, 0, alignment=Qt.AlignRight)
        grid.addWidget(self.frame_skip, 2, 1)

        grid.addWidget(QLabel("Serial Port:"), 2, 2, alignment=Qt.AlignRight)
        grid.addWidget(self.serial_port, 2, 3)

        grid.addWidget(QLabel("Baudrate:"), 3, 0, alignment=Qt.AlignRight)
        grid.addWidget(self.serial_baud, 3, 1)

        for i in range(grid.count()):
            item = grid.itemAt(i).widget()
            if isinstance(item, QLabel):
                item.setStyleSheet(label_style)

        self.save_button = QPushButton(" Save")
        self.save_button.setIcon(get_icon("save.png"))
        self.save_button.setIconSize(QSize(28, 28))
        self.save_button.setStyleSheet(self.styles.button())
        self.save_button.setFixedHeight(45)
        self.save_button.clicked.connect(self._save_settings)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.setContentsMargins(0, 0, 20, 0)

        # ======================
        # MAIN LAYOUT
        # ======================
        layout.addLayout(grid)
        layout.addLayout(button_layout)
        layout.addStretch()
        self.setLayout(layout)

    def _load_settings(self):
        if not os.path.exists(self.settings_file):
            return
        try:
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
                yolo_model_name = settings.get("YOLO_MODEL", "small-tree")

                if yolo_model_name in [
                    self.yolo_model.itemText(i) for i in range(self.yolo_model.count())
                ]:
                    self.yolo_model.setCurrentText(yolo_model_name)

                self.camera_index.setText(str(settings.get("CAMERA_INDEX", 0)))
                self.img_size.setText(str(settings.get("YOLO_IMAGE_SIZE", 320)))
                self.conf.setText(str(settings.get("YOLO_CONFIDENCE", 0.4)))
                self.frame_skip.setText(str(settings.get("YOLO_FRAME_SKIP", 5)))
                self.serial_port.setText(settings.get("SERIAL_PORT", "/dev/ttyUSB0"))
                self.serial_baud.setText(str(settings.get("SERIAL_BAUDRATE", 9600)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load settings: {e}")
            add_log(
                LogLevel.ERROR.value,
                LogSource.UI_SETTINGS.value,
                f"Failed to load settings: {e}",
            )

    def _save_settings(self):
        selected_model = self.yolo_model.currentText()
        model_path = os.path.join(self.models_path, f"{selected_model}.pt")

        data = {
            "YOLO_MODEL": selected_model,
            "MODEL_PATH": model_path,
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
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            add_log(
                LogLevel.INFO.value,
                LogSource.UI_SETTINGS.value,
                "Settings saved successfully",
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")
            add_log(
                LogLevel.ERROR.value,
                LogSource.UI_SETTINGS.value,
                f"Failed to save settings: {e}",
            )

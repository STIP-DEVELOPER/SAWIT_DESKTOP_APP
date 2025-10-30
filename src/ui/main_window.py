from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
)
from PyQt5.QtCore import Qt
from src.configs import config


class MainWindow(QWidget):
    """UI layout for Dual Camera YOLO Detector"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.WINDOW_TITLE)
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self._build_ui()

    def _build_ui(self):
        # Camera labels
        self.left_label = QLabel("Camera Left")
        self.right_label = QLabel("Camera Right")

        # Log display
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        # Buttons
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.exit_button = QPushButton("Exit")

        # Layout: buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.exit_button)

        # Layout: camera views
        camera_layout = QHBoxLayout()
        camera_layout.addWidget(self.left_label)
        camera_layout.addWidget(self.right_label)

        # Final layout
        layout = QVBoxLayout()
        layout.addLayout(camera_layout)
        layout.addWidget(self.log_box)
        layout.addLayout(button_layout)

        self.setLayout(layout)

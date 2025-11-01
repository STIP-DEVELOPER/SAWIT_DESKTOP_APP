from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
)
from PyQt5.QtCore import Qt
from configs import config


class MainWindow(QWidget):
    """UI layout for Single Camera YOLO Detector"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.WINDOW_TITLE)
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.show_camera = True  # <--- add state variable
        self._build_ui()

    def _build_ui(self):
        # ======================
        # CAMERA VIEW AREA
        # ======================
        self.camera_label = QLabel("Camera View")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setFixedSize(640, 480)
        self.camera_label.setStyleSheet(
            """
            border: 2px solid #444;
            background-color: #111;
            color: #aaa;
            font-size: 14px;
        """
        )

        # ======================
        # LOG BOX
        # ======================
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

        # ======================
        # BUTTONS
        # ======================
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.toggle_camera_button = QPushButton("Hide Camera")  # <--- new button
        self.exit_button = QPushButton("Exit")

        button_style = """
            QPushButton {
                background-color: #333;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #222;
            }
        """
        self.start_button.setStyleSheet(button_style)
        self.stop_button.setStyleSheet(button_style)
        self.toggle_camera_button.setStyleSheet(button_style)
        self.exit_button.setStyleSheet(button_style)

        # ======================
        # LAYOUT
        # ======================
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.toggle_camera_button)
        button_layout.addWidget(self.exit_button)
        button_layout.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.camera_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.log_box)
        layout.addLayout(button_layout)

        self.setLayout(layout)

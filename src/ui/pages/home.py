from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.show_camera = True
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        # Camera preview area
        self.camera_label = QLabel("Camera View")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.camera_label.setStyleSheet(
            """
            border: 2px solid #444;
            background-color: #111;
            color: #aaa;
            font-size: 14px;
        """
        )

        # Log box
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

        # Buttons
        self.start_button = QPushButton("▶ Start")
        self.stop_button = QPushButton("⏹ Stop")
        self.toggle_camera_button = QPushButton("👁 Show/Hide Camera")
        self.exit_button = QPushButton("⏻ Exit")

        for btn in [
            self.start_button,
            self.stop_button,
            self.toggle_camera_button,
            self.exit_button,
        ]:
            btn.setStyleSheet(self._button_style())

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.toggle_camera_button)
        control_layout.addWidget(self.exit_button)

        layout.addWidget(self.camera_label)
        layout.addWidget(self.log_box)
        layout.addLayout(control_layout)
        layout.setStretch(0, 3)
        layout.setStretch(1, 1)

        self.setLayout(layout)

    def _button_style(self):
        return """
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

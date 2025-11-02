import os
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QHBoxLayout,
    QSizePolicy,
    QToolButton,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.show_camera = True
        self.is_running = False  # status start/stop
        self._build_ui()

    def _icon(self, name: str) -> QIcon:
        icon_path = os.path.join(os.getcwd(), "assets", "icons", name)
        return QIcon(icon_path) if os.path.exists(icon_path) else QIcon()

    def _build_ui(self):
        layout = QVBoxLayout()

        # ======================
        # CAMERA VIEW
        # ======================
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

        # ======================
        # LOG VIEW
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
        # CONTROL BUTTONS
        # ======================
        self.start_button = QToolButton()
        self.start_button.setText("Start")
        self.start_button.setIcon(self._icon("start.png"))
        self.start_button.setIconSize(QSize(28, 28))
        self.start_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.start_button.setLayoutDirection(Qt.LeftToRight)
        self.start_button.clicked.connect(self.toggle_start_stop)

        self.stop_button = QToolButton()
        self.stop_button.setText("Stop")
        self.stop_button.setIcon(self._icon("stop.png"))
        self.stop_button.setIconSize(QSize(28, 28))
        self.stop_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.stop_button.setLayoutDirection(Qt.LeftToRight)
        self.stop_button.clicked.connect(self.toggle_start_stop)
        self.stop_button.hide()  # disembunyikan di awal

        self.toggle_camera_button = QToolButton()
        self.toggle_camera_button.setText("Camera")
        self.toggle_camera_button.setIcon(self._icon("camera.png"))
        self.toggle_camera_button.setIconSize(QSize(28, 28))
        self.toggle_camera_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_camera_button.setLayoutDirection(Qt.LeftToRight)

        # Styling
        for btn in [
            self.start_button,
            self.stop_button,
            self.toggle_camera_button,
        ]:
            btn.setStyleSheet(self._button_style())
            btn.setFixedHeight(40)

        # Control layout
        control_layout = QHBoxLayout()
        control_layout.setSpacing(20)
        control_layout.setAlignment(Qt.AlignCenter)
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.toggle_camera_button)

        # ======================
        # LAYOUT STRUCTURE
        # ======================
        layout.addWidget(self.camera_label)
        layout.addWidget(self.log_box)
        layout.addLayout(control_layout)
        layout.setStretch(0, 3)
        layout.setStretch(1, 1)
        self.setLayout(layout)

    def toggle_start_stop(self):
        """Ganti tombol Start/Stop"""
        self.is_running = not self.is_running
        if self.is_running:
            self.start_button.hide()
            self.stop_button.show()
            self.log_box.append("▶️ Inference started...")
        else:
            self.stop_button.hide()
            self.start_button.show()
            self.log_box.append("⏹ Inference stopped.")

    def _button_style(self):
        return """
            QToolButton {
                background-color: #222;
                border-radius: 6px;
                color: white;
                font-size: 14px;
                padding: 6px 14px;
            }
            QToolButton:hover { background-color: #444; }
            QToolButton:pressed { background-color: #000; }
        """

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QHBoxLayout,
    QSizePolicy,
    QToolButton,
)
from PyQt5.QtCore import Qt, QSize

from core.logger import add_log
from enums.log import LogLevel, LogSource
from helpers.format_log import format_log_text
from helpers.icon import get_icon
from ui.pages.home.styles import HomePageStyle


class HomePage(QWidget, HomePageStyle):
    styles = HomePageStyle()

    def __init__(self):
        super().__init__()
        self.show_camera = True
        self.is_running = False
        self._build_ui()

    def _build_ui(self):
        # ======================
        # CAMERA CONTAINER
        # ======================
        self.camera_container = QWidget(self)
        self.camera_container.setStyleSheet("background-color: transparent;")
        self.camera_container.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.camera_container_layout = QVBoxLayout(self.camera_container)
        self.camera_container_layout.setContentsMargins(0, 0, 0, 0)

        # Kamera utama
        self.camera_label = QLabel("Camera View")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.camera_label.setStyleSheet(self.styles.camera_style())
        self.camera_container_layout.addWidget(self.camera_label)

        # ======================
        # LOG OVERLAY (pojok kanan atas)
        # ======================
        self.log_box = QTextEdit(self.camera_container)
        self.log_box.setReadOnly(True)
        self.log_box.setFixedWidth(300)
        self.log_box.setFixedHeight(150)
        self.log_box.move(960, 20)
        self.log_box.setStyleSheet(self.styles.log_style())

        # ======================
        # CONTROL BUTTONS
        # ======================
        self.start_button = QToolButton()
        self.start_button.setText("Start")
        self.start_button.setIcon(get_icon("start.png"))
        self.start_button.setIconSize(QSize(28, 28))
        self.start_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.start_button.clicked.connect(self.toggle_start_stop)

        self.stop_button = QToolButton()
        self.stop_button.setText("Stop")
        self.stop_button.setIcon(get_icon("stop.png"))
        self.stop_button.setIconSize(QSize(28, 28))
        self.stop_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.stop_button.clicked.connect(self.toggle_start_stop)
        self.stop_button.hide()

        self.toggle_camera_button = QToolButton()
        self.toggle_camera_button.setText("Camera")
        self.toggle_camera_button.setIcon(get_icon("camera.png"))
        self.toggle_camera_button.setIconSize(QSize(28, 28))
        self.toggle_camera_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        for btn in [self.start_button, self.stop_button, self.toggle_camera_button]:
            btn.setStyleSheet(self.styles.button_style())
            btn.setFixedHeight(40)

        control_layout = QHBoxLayout()
        control_layout.setSpacing(20)
        control_layout.setAlignment(Qt.AlignCenter)
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.toggle_camera_button)

        # ======================
        # MAIN LAYOUT
        # ======================
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.camera_container)
        main_layout.addLayout(control_layout)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 0)
        self.setLayout(main_layout)

    # ======================
    # FUNCTIONAL
    # ======================

    def toggle_start_stop(self):
        """Toggle inference start/stop state."""
        self.is_running = not self.is_running
        if self.is_running:
            self.start_button.hide()
            self.stop_button.show()
            self._append_log(
                format_log_text(
                    source=LogSource.UI_HOME.value,
                    message=f"Inference started...",
                )
            )
            add_log(LogLevel.INFO.value, LogSource.UI_HOME.value, "Inference started")
        else:
            self.stop_button.hide()
            self.start_button.show()

            self._append_log(
                format_log_text(
                    source=LogSource.UI_HOME.value,
                    message=f"Inference Stopped...",
                )
            )
            add_log(LogLevel.INFO.value, LogSource.UI_HOME.value, "Inference stopped")

    def _append_log(self, text: str):
        """Append message to overlay log box."""
        self.log_box.append(text)
        self.log_box.verticalScrollBar().setValue(
            self.log_box.verticalScrollBar().maximum()
        )

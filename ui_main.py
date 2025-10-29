from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
)
from PyQt5.QtCore import Qt


class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Sawit Detection System")
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f6f8fa;
                font-family: Arial;
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1976d2;
                color: white;
                border-radius: 6px;
                padding: 6px 10px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QTextEdit {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
        """
        )

        # --- Video feed section ---
        self.video_left = QLabel("Video Kiri")
        self.video_left.setFixedSize(320, 240)
        self.video_left.setStyleSheet("background-color: #ddd; border-radius: 8px;")

        self.video_right = QLabel("Video Kanan")
        self.video_right.setFixedSize(320, 240)
        self.video_right.setStyleSheet("background-color: #ddd; border-radius: 8px;")

        video_layout = QHBoxLayout()
        video_layout.addWidget(self.video_left)
        video_layout.addWidget(self.video_right)

        video_group = QGroupBox("Kamera")
        video_group.setLayout(video_layout)

        # --- Control section ---
        self.label_distance = QLabel("Distance: --- m")
        self.label_status = QLabel("Status: ---")

        self.btn_motor_on = QPushButton("Aktifkan Motor")
        self.btn_motor_off = QPushButton("Matikan Motor")
        self.btn_auto_mode = QPushButton("Mode Otomatis: OFF")

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.label_distance)
        control_layout.addWidget(self.label_status)
        control_layout.addWidget(self.btn_motor_on)
        control_layout.addWidget(self.btn_motor_off)
        control_layout.addWidget(self.btn_auto_mode)

        control_group = QGroupBox("Kontrol")
        control_group.setLayout(control_layout)

        # --- Log section ---
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.append("[System] Initialized...")

        log_group = QGroupBox("Log Aktivitas")
        log_layout = QVBoxLayout()
        log_layout.addWidget(self.log_box)
        log_group.setLayout(log_layout)

        # --- Main layout ---
        layout = QVBoxLayout()
        layout.addWidget(video_group)
        layout.addWidget(control_group)
        layout.addWidget(log_group)

        self.setLayout(layout)

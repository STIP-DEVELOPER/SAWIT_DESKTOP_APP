from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from core.camera_handler import CameraThread


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Pemupuk Otomatis Sawit")
        self.setGeometry(100, 100, 1200, 700)

        # === WIDGET UTAMA ===
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # === LABEL UNTUK VIDEO FEED ===
        self.label_camera_left = QLabel("Kamera Kiri")
        self.label_camera_right = QLabel("Kamera Kanan")
        self.label_camera_left.setAlignment(Qt.AlignCenter)
        self.label_camera_right.setAlignment(Qt.AlignCenter)
        self.label_camera_left.setStyleSheet("background-color: #2c3e50; color: white;")
        self.label_camera_right.setStyleSheet(
            "background-color: #2c3e50; color: white;"
        )

        # === LOG PANEL ===
        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)

        # === BUTTON CONTROL ===
        self.btn_manual_on = QPushButton("🔆 Aktifkan Motor")
        self.btn_manual_off = QPushButton("💤 Matikan Motor")

        # === LAYOUT SETUP ===
        layout = QGridLayout()
        layout.addWidget(self.label_camera_left, 0, 0)
        layout.addWidget(self.label_camera_right, 0, 1)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_manual_on)
        button_layout.addWidget(self.btn_manual_off)
        layout.addLayout(button_layout, 1, 0, 1, 2)

        layout.addWidget(QLabel("Log Aktivitas:"), 2, 0, 1, 2)
        layout.addWidget(self.text_log, 3, 0, 1, 2)
        central_widget.setLayout(layout)

        # === INISIASI KAMERA ===
        self.init_cameras()

    def init_cameras(self):
        self.camera_left = CameraThread(0, "left")  # kamera 0
        self.camera_right = CameraThread(1, "right")  # kamera 1

        self.camera_left.frame_update.connect(self.update_frame)
        self.camera_right.frame_update.connect(self.update_frame)

        self.camera_left.start()
        self.camera_right.start()

    def update_frame(self, image, camera_name):
        if camera_name == "left":
            self.label_camera_left.setPixmap(QPixmap.fromImage(image))
        elif camera_name == "right":
            self.label_camera_right.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        self.camera_left.stop()
        self.camera_right.stop()
        event.accept()

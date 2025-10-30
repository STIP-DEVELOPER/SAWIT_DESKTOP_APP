from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QTextEdit,
    QGridLayout,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from core.yolo_detector import YoloDetector
import sys
import cv2
import numpy as np


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Pemupuk Otomatis Sawit")
        self.setGeometry(100, 100, 1200, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # --- Label Kamera ---
        self.label_camera_left = QLabel("Kamera Kiri")
        self.label_camera_right = QLabel("Kamera Kanan")

        for label in [self.label_camera_left, self.label_camera_right]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(
                "background-color: #2c3e50; color: white; font-size: 18px;"
            )

        # --- Log ---
        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)

        # --- Layout ---
        layout = QGridLayout()
        layout.addWidget(self.label_camera_left, 0, 0)
        layout.addWidget(self.label_camera_right, 0, 1)
        layout.addWidget(QLabel("Log Aktivitas:"), 1, 0, 1, 2)
        layout.addWidget(self.text_log, 2, 0, 1, 2)
        central_widget.setLayout(layout)

        # --- Inisialisasi Kamera ---
        self.init_cameras()

    def init_cameras(self):
        """Inisialisasi dua kamera (kiri dan kanan)"""
        # Kamera kiri
        self.camera_left = YoloDetector(0, side_name="Sawit Kiri")
        self.camera_left.frame_update.connect(
            lambda frame: self.update_frame(frame, "left")
        )
        self.camera_left.detection_update.connect(lambda side: self.log_detection(side))
        self.camera_left.start()

        # Kamera kanan (fallback ke kamera 0 jika 1 gagal)
        self.camera_right = YoloDetector(1, side_name="Sawit Kanan")
        self.camera_right.frame_update.connect(
            lambda frame: self.update_frame(frame, "right")
        )
        self.camera_right.detection_update.connect(
            lambda side: self.log_detection(side)
        )
        self.camera_right.start()

    def update_frame(self, frame, camera_name):
        """Menampilkan frame ke label GUI"""
        if frame is None or not isinstance(frame, np.ndarray):
            print(f"[WARNING] Frame {camera_name} kosong atau invalid — dilewati.")
            return

        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"[ERROR] cvtColor gagal di kamera {camera_name}: {e}")
            return

        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)

        if camera_name == "left":
            self.label_camera_left.setPixmap(pixmap)
        else:
            self.label_camera_right.setPixmap(pixmap)

    def log_detection(self, side):
        """Menampilkan log deteksi"""
        self.text_log.append(f"✅ Detected: {side}")

    def closeEvent(self, event):
        """Menutup thread kamera ketika aplikasi ditutup"""
        self.camera_left.stop()
        self.camera_right.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())

import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QGridLayout,
    QMessageBox,
)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap

from core.camera_capture import CameraCapture
from core.inference_worker import InferenceWorker
from core.utils import frame_to_qpixmap

import cv2


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAWIT - Sistem Pemupuk Otomatis")
        self.setMinimumSize(1000, 700)

        self.left_label = QLabel("Left Camera")
        self.left_label.setAlignment(Qt.AlignCenter)
        self.left_label.setFixedSize(480, 360)
        self.left_label.setStyleSheet("background: #333; color: #fff;")

        self.right_label = QLabel("Right Camera")
        self.right_label.setAlignment(Qt.AlignCenter)
        self.right_label.setFixedSize(480, 360)
        self.right_label.setStyleSheet("background: #333; color: #fff;")

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(150)

        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.exit_btn = QPushButton("Exit")
        self.stop_btn.setEnabled(False)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.exit_btn)

        grid = QGridLayout()
        grid.addWidget(self.left_label, 0, 0)
        grid.addWidget(self.right_label, 0, 1)
        grid.addLayout(btn_layout, 1, 0, 1, 2)
        grid.addWidget(self.log, 2, 0, 1, 2)

        self.setLayout(grid)

        # threads
        backend = None
        try:
            backend = cv2.CAP_AVFOUNDATION
        except Exception:
            backend = None

        self.cam_left = CameraCapture(index=0, name="Kiri", fps=20, backend=backend)
        self.cam_right = CameraCapture(index=1, name="Kanan", fps=20, backend=backend)

        models_dir = os.path.join(os.path.dirname(__file__), "models")
        model_path = os.path.join(models_dir, "yolov5n.pt")
        self.infer = InferenceWorker(model_path=model_path, conf=0.35, imgsz=640)

        # connections
        self.start_btn.clicked.connect(self.start_all)
        self.stop_btn.clicked.connect(self.stop_all)
        self.exit_btn.clicked.connect(self.close_app)

        self.cam_left.frame_ready.connect(self.on_left_frame)
        self.cam_right.frame_ready.connect(self.on_right_frame)
        self.cam_left.error.connect(self.on_error)
        self.cam_right.error.connect(self.on_error)

        self.infer.frame_processed.connect(self.on_infer_frame)
        self.infer.log.connect(self.log_message)
        self.infer.model_ready.connect(self.on_model_ready)

        self.last_left_frame = None
        self.last_right_frame = None

    @pyqtSlot(object)
    def on_left_frame(self, frame):
        self.last_left_frame = frame.copy()
        pix = frame_to_qpixmap(frame)
        self.left_label.setPixmap(
            pix.scaled(self.left_label.size(), Qt.KeepAspectRatio)
        )

        # send to inference (you may choose to send only one stream or both)
        self.infer.submit_frame(frame)

    @pyqtSlot(object)
    def on_right_frame(self, frame):
        self.last_right_frame = frame.copy()
        pix = frame_to_qpixmap(frame)
        self.right_label.setPixmap(
            pix.scaled(self.right_label.size(), Qt.KeepAspectRatio)
        )

        # optionally send right frame to inference as well:
        # self.infer.submit_frame(frame)

    @pyqtSlot(object)
    def on_infer_frame(self, frame):
        pix = frame_to_qpixmap(frame)
        # show inference result on the left preview (design choice)
        self.left_label.setPixmap(
            pix.scaled(self.left_label.size(), Qt.KeepAspectRatio)
        )

    @pyqtSlot(str)
    def on_error(self, msg):
        self.log_message(f"[ERROR] {msg}")

    @pyqtSlot(bool)
    def on_model_ready(self, ok):
        if ok:
            self.log_message("Model inference siap.")
        else:
            self.log_message("Model inference gagal diinisialisasi.")

    def log_message(self, msg: str):
        from datetime import datetime

        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log.append(f"[{t}] {msg}")

    def start_all(self):
        self.log_message("Memulai kamera dan inference...")
        # start inference thread first to initialize model
        if not self.infer.isRunning():
            self.infer.start()
        # start cameras
        if not self.cam_left.isRunning():
            self.cam_left.start()
        if not self.cam_right.isRunning():
            self.cam_right.start()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_all(self):
        self.log_message("Menghentikan kamera dan inference...")
        if self.cam_left.isRunning():
            self.cam_left.stop()
        if self.cam_right.isRunning():
            self.cam_right.stop()
        if self.infer.isRunning():
            self.infer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def close_app(self):
        self.stop_all()
        self.log_message("Keluar aplikasi.")
        self.close()

    def closeEvent(self, event):
        self.stop_all()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

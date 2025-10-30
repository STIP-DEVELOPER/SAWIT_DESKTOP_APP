import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
)
from PyQt5.QtCore import Qt
from core.camera_capture import CameraCapture
from core.inference_worker import InferenceWorker
from core.utils import convert_frame_to_qpixmap
from core import config


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.WINDOW_TITLE)
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        # === UI Components ===
        self.left_label = QLabel("Camera Left")
        self.right_label = QLabel("Camera Right")
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.exit_button = QPushButton("Exit")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.exit_button)

        camera_layout = QHBoxLayout()
        camera_layout.addWidget(self.left_label)
        camera_layout.addWidget(self.right_label)

        layout = QVBoxLayout()
        layout.addLayout(camera_layout)
        layout.addWidget(self.log_box)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # === Components ===
        self.left_camera = CameraCapture(config.LEFT_CAMERA_INDEX)
        self.right_camera = CameraCapture(config.RIGHT_CAMERA_INDEX)
        self.inference_worker = InferenceWorker(
            model_path=config.YOLO_MODEL_PATH,
            imgsz=config.YOLO_IMAGE_SIZE,
            conf=config.YOLO_CONFIDENCE,
        )

        # === Connections ===
        self.left_camera.frame_ready.connect(self.on_left_frame)
        self.right_camera.frame_ready.connect(self.on_right_frame)
        self.inference_worker.frame_processed.connect(self.on_inference_result)
        self.inference_worker.log.connect(self.append_log)

        self.start_button.clicked.connect(self.start_cameras)
        self.stop_button.clicked.connect(self.stop_cameras)
        self.exit_button.clicked.connect(self.close)

        self.latest_left_frame = None
        self.latest_right_frame = None

    # =====================================================
    # Camera & Worker Control
    # =====================================================

    def start_cameras(self):
        self.append_log("[System] Starting cameras...")
        self.inference_worker.start()
        self.left_camera.start()
        self.right_camera.start()

    def stop_cameras(self):
        self.append_log("[System] Stopping cameras...")
        self.left_camera.stop()
        self.right_camera.stop()
        self.inference_worker.stop()

    def closeEvent(self, event):
        self.stop_cameras()
        event.accept()

    # =====================================================
    # Frame Handlers
    # =====================================================

    def on_left_frame(self, frame):
        """Terima frame dari kamera kiri"""
        self.latest_left_frame = frame
        if frame is not None:
            self.update_camera_view(self.left_label, frame)
            self.inference_worker.submit_frame(("left", frame))

    def on_right_frame(self, frame):
        """Terima frame dari kamera kanan"""
        self.latest_right_frame = frame
        if frame is not None:
            self.update_camera_view(self.right_label, frame)
            self.inference_worker.submit_frame(("right", frame))

    def on_inference_result(self, result):
        """Terima hasil deteksi YOLO"""
        if not isinstance(result, tuple) or len(result) != 2:
            return
        side, frame = result
        if side == "left":
            self.update_camera_view(self.left_label, frame)
        elif side == "right":
            self.update_camera_view(self.right_label, frame)

    # =====================================================
    # Utility
    # =====================================================

    def update_camera_view(self, label, frame):
        pixmap = convert_frame_to_qpixmap(frame)
        label.setPixmap(pixmap)

    def append_log(self, text):
        self.log_box.append(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

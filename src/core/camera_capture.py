import cv2
import time
from PyQt5.QtCore import QThread, pyqtSignal
from configs import config
from core.logger import add_log


class CameraCapture(QThread):
    frame_ready = pyqtSignal(object)
    log = pyqtSignal(str)

    def __init__(self, camera_index=0, name="left", parent=None):
        super().__init__(parent)
        self.camera_index = camera_index
        self.name = name
        self.cap = None
        self.running = False

    def run(self):
        self.running = True
        try:
            self.cap = cv2.VideoCapture(self.camera_index, config.CAMERA_BACKEND)
            if not self.cap.isOpened():
                self.log.emit(
                    f"[Camera-{self.name}] Tidak dapat membuka kamera {self.camera_index}."
                )
                return
            self.log.emit(f"[Camera-{self.name}] Kamera {self.camera_index} aktif.")

            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    self.log.emit(f"[Camera-{self.name}] Gagal membaca frame.")
                    add_log(
                        "ERROR",
                        f"Camera-{self.name}",
                        "Gagal membaca frame dari kamera.",
                    )
                    time.sleep(0.1)
                    continue
                self.frame_ready.emit(frame)
                time.sleep(config.FRAME_DELAY)

        except Exception as e:
            self.log.emit(f"[Camera-{self.name}] Error: {e}")
            add_log("ERROR", f"Camera-{self.name}", f"Error kamera: {e}")
        finally:
            if self.cap:
                self.cap.release()
                self.log.emit(f"[Camera-{self.name}] Dihentikan.")
                add_log("INFO", f"Camera-{self.name}", "Kamera dihentikan.")

    def stop(self):
        self.running = False
        self.wait()

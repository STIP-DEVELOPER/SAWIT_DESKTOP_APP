from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import time


class CameraCapture(QThread):
    frame_ready = pyqtSignal(object)  # numpy frame
    error = pyqtSignal(str)

    def __init__(self, index=0, name="Camera", fps=20, backend=None, parent=None):
        super().__init__(parent)
        self.index = index
        self.name = name
        self.fps = fps
        self._running = False
        self.cap = None
        self.backend = backend

    def run(self):
        try:
            if self.backend is not None:
                self.cap = cv2.VideoCapture(self.index, self.backend)
            else:
                self.cap = cv2.VideoCapture(self.index)
            if not self.cap or not self.cap.isOpened():
                self.error.emit(
                    f"{self.name}: Tidak dapat membuka kamera index={self.index}"
                )
                return

            self._running = True
            interval = 1.0 / max(1, self.fps)
            while self._running:
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    self.error.emit(
                        f"{self.name}: Gagal membaca frame dari kamera index={self.index}"
                    )
                    time.sleep(0.2)
                    continue
                self.frame_ready.emit(frame)
                time.sleep(interval)
        except Exception as e:
            self.error.emit(f"{self.name}: Exception: {e}")
        finally:
            if self.cap and self.cap.isOpened():
                self.cap.release()
            self._running = False

    def stop(self):
        self._running = False
        self.wait(timeout=2000)

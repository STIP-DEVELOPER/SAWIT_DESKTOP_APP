import cv2
import time
from PyQt5.QtCore import QThread, pyqtSignal
from core.logger import add_log
from configs import config


class VideoCaptureThread(QThread):
    """
    Reads video file frame by frame and emits frame_ready signal.
    Similar interface to CameraCapture for seamless integration.
    """
    frame_ready = pyqtSignal(object)
    log = pyqtSignal(str)

    def __init__(self, video_path, name="video", parent=None):
        super().__init__(parent)
        self.video_path = video_path
        self.name = name
        self.cap = None
        self.running = False

    def run(self):
        self.running = True
        try:
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                self.log.emit(f"[Video-{self.name}] Cannot open video {self.video_path}.")
                add_log("ERROR", f"Video-{self.name}", f"Cannot open video {self.video_path}.")
                return
            self.log.emit(f"[Video-{self.name}] Video {self.video_path} opened successfully.")

            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    self.log.emit(f"[Video-{self.name}] End of video or failed to read frame.")
                    break
                self.frame_ready.emit(frame)
                time.sleep(config.FRAME_DELAY)  # same delay as camera

        except Exception as e:
            self.log.emit(f"[Video-{self.name}] Error: {e}")
            add_log("ERROR", f"Video-{self.name}", f"Video capture error: {e}")
        finally:
            if self.cap:
                self.cap.release()
                self.log.emit(f"[Video-{self.name}] Stopped.")
                add_log("INFO", f"Video-{self.name}", "Video capture stopped.")

    def stop(self):
        self.running = False
        self.wait()

import cv2
import time
from PyQt5.QtCore import QThread, pyqtSignal
from configs import config
from core.logger import add_log
from enums.log import LogLevel, LogSource
from helpers.format_log import format_log_text


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
                    format_log_text(
                        source=LogSource.CORE_CAMERA.value,
                        message=f"can't open camera {self.camera_index}",
                    )
                )
                return

            self.log.emit(
                format_log_text(
                    source=LogSource.CORE_CAMERA.value,
                    message=f"camera {self.name} {self.camera_index} is cative.",
                )
            )

            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    self.log.emit(
                        format_log_text(
                            source=LogSource.CORE_CAMERA.value,
                            message=f"camera {self.name} failed open frame",
                        )
                    )

                    add_log(
                        LogLevel.ERROR.value,
                        f"Camera-{self.name}",
                        "Can't read frame from camera",
                    )
                    # time.sleep(0.1)
                    continue

                self.frame_ready.emit(frame)
                time.sleep(config.FRAME_DELAY)

        except Exception as e:
            self.log.emit(
                format_log_text(
                    source=LogSource.CORE_CAMERA.value,
                    message=f"camera {self.name} Error: {e}",
                )
            )

            add_log(
                LogLevel.ERROR.value,
                f"Camera-{self.name}",
                f"Error: {e}",
            )

        finally:
            if self.cap:
                self.cap.release()
                self.log.emit(
                    format_log_text(
                        source=LogSource.CORE_CAMERA.value,
                        message=f"camera {self.name} was stoped",
                    )
                )

                add_log(
                    LogLevel.INFO.value,
                    f"Camera-{self.name}",
                    "Camera was stoped",
                )

    def stop(self):
        self.running = False
        self.wait()

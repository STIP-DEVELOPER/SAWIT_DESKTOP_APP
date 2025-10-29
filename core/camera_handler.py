import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage


class CameraThread(QThread):
    frame_update = pyqtSignal(QImage, str)

    def __init__(self, camera_id: int, camera_name: str):
        super().__init__()
        self.camera_id = camera_id
        self.camera_name = camera_name
        self.cap = None
        self.running = False

    def run(self):
        self.cap = cv2.VideoCapture(self.camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.running = True

        while self.running:
            ret, frame = self.cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(
                    rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888
                )
                scaled_img = qt_image.scaled(600, 400)
                self.frame_update.emit(scaled_img, self.camera_name)
        self.cap.release()

    def stop(self):
        self.running = False
        self.wait()

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
import cv2
from ultralytics import YOLO


class YoloDetector(QThread):
    frame_update = pyqtSignal(QImage)
    detection_update = pyqtSignal(str)  # Kirim "Kiri" atau "Kanan" jika terdeteksi

    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.cap = None
        self.running = False
        self.model = YOLO("yolov5n.pt")  # Bisa ganti dengan model custom kamu

    def run(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.running = True

        while self.running:
            ret, frame = self.cap.read()
            if ret:
                results = self.model.predict(frame, verbose=False)  # jalankan inference

                # Loop tiap deteksi
                for result in results:
                    boxes = result.boxes.xyxy
                    class_ids = result.boxes.cls
                    for i, box in enumerate(boxes):
                        x1, y1, x2, y2 = map(int, box)
                        label = (
                            "Sawit Kiri" if self.camera_index == 0 else "Sawit Kanan"
                        )
                        color = (0, 255, 0) if self.camera_index == 0 else (0, 0, 255)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(
                            frame,
                            label,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            color,
                            2,
                        )
                        self.detection_update.emit(label)  # kirim sisi terdeteksi

                # Konversi ke QImage
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(
                    rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888
                )
                self.frame_update.emit(qt_image)

        self.cap.release()

    def stop(self):
        self.running = False
        self.wait()

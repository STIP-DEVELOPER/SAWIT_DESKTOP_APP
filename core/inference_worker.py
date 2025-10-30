import time
import cv2
import numpy as np
from collections import deque
from PyQt5.QtCore import QThread, pyqtSignal
from ultralytics import YOLO
from core.utils import draw_boxes_on_frame
from core import config


class InferenceWorker(QThread):
    frame_processed = pyqtSignal(tuple)  # (side, frame)
    log = pyqtSignal(str)

    def __init__(
        self, model_path="models/yolov5n.pt", imgsz=320, conf=0.4, parent=None
    ):
        super().__init__(parent)
        self.model_path = model_path
        self.imgsz = imgsz
        self.conf = conf
        self.running = False

        # Dua queue terpisah: kamera kiri & kanan
        self.frame_queue = {
            "left": deque(maxlen=config.QUEUE_MAXLEN),
            "right": deque(maxlen=config.QUEUE_MAXLEN),
        }

        # Round-robin tracker
        self.last_side = "right"
        self.model = None

    def run(self):
        self.running = True
        self._load_model()

        while self.running:
            # Tentukan giliran kamera berikutnya
            side = "left" if self.last_side == "right" else "right"

            # Jika queue kamera ini punya frame, proses
            if self.frame_queue[side]:
                frame = self.frame_queue[side].popleft()
                self._process_frame(side, frame)
                self.last_side = side
            # Jika tidak ada frame di kamera ini, coba kamera satunya
            elif self.frame_queue["left" if side == "right" else "right"]:
                alt_side = "left" if side == "right" else "right"
                frame = self.frame_queue[alt_side].popleft()
                self._process_frame(alt_side, frame)
                self.last_side = alt_side
            else:
                # Tidak ada frame baru, istirahat sebentar
                time.sleep(0.01)

    def stop(self):
        self.running = False
        self.wait()

    def submit_frame(self, data):
        """
        Menerima frame dari main.py -> (side, frame)
        """
        if not self.running:
            return
        side, frame = data
        if side not in self.frame_queue:
            return
        self.frame_queue[side].append(frame)

    # -----------------------------
    # INTERNAL
    # -----------------------------

    def _load_model(self):
        """
        Load model YOLO dari ultralytics.
        Auto-download jika belum ada.
        """
        try:
            self.log.emit(f"[Inference] Memuat model dari: {self.model_path}")
            self.model = YOLO(self.model_path)
            self.log.emit(f"[Inference] Model '{self.model_path}' berhasil dimuat.")
        except Exception as e:
            self.log.emit(f"[Inference] Gagal memuat model lokal: {e}")
            self.log.emit("[Inference] Mencoba model default 'yolov8n.pt' ...")
            try:
                self.model = YOLO("yolov8n.pt")
                self.log.emit(
                    "[Inference] Model 'yolov8n.pt' berhasil dimuat (fallback)."
                )
            except Exception as e2:
                self.log.emit(f"[Inference] Gagal memuat model fallback: {e2}")
                self.running = False

    def _process_frame(self, side, frame):
        """
        Jalankan YOLO pada satu frame.
        """
        if self.model is None:
            return

        try:
            # Jalankan YOLO inference
            results = self.model.predict(
                source=frame, imgsz=self.imgsz, conf=self.conf, verbose=False
            )

            # Ambil hasil deteksi dari frame pertama
            res = results[0]
            boxes = res.boxes.xyxy.cpu().numpy() if len(res.boxes) > 0 else []
            labels = (
                [res.names[int(c)] for c in res.boxes.cls.cpu().numpy()]
                if len(res.boxes) > 0
                else []
            )
            confs = res.boxes.conf.cpu().numpy() if len(res.boxes) > 0 else []

            # Gambar kotak hasil deteksi
            frame_out = draw_boxes_on_frame(frame, boxes, labels, confs)

            # Emit hasil ke GUI
            self.frame_processed.emit((side, frame_out))

            # Log ringkas
            self.log.emit(f"[Inference-{side}] {len(boxes)} objek terdeteksi.")
        except Exception as e:
            self.log.emit(f"[Inference-{side}] Error: {e}")

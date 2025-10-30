from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import numpy as np
import time
import os


class InferenceWorker(QThread):
    frame_processed = pyqtSignal(object)  # processed frame (numpy)
    log = pyqtSignal(str)
    model_ready = pyqtSignal(bool)

    def __init__(self, model_path=None, conf=0.35, imgsz=640, parent=None):
        super().__init__(parent)
        self._running = False
        self._queue = []
        self.model_path = model_path
        self.conf = conf
        self.imgsz = imgsz
        self.model = None

    def run(self):
        try:
            from ultralytics import YOLO
        except Exception as e:
            self.log.emit(f"Inference: gagal import ultralytics: {e}")
            return

        try:
            if self.model_path and os.path.exists(self.model_path):
                self.model = YOLO(self.model_path)
                self.log.emit(f"Inference: memuat model dari {self.model_path}")
            else:
                # coba load via model name sehingga ultralytics mungkin mengunduhnya otomatis
                try:
                    self.model = YOLO("yolov5n.pt")
                    self.log.emit(
                        "Inference: memuat model 'yolov5n.pt' via ultralytics"
                    )
                except Exception:
                    try:
                        self.model = YOLO("yolov5n")
                        self.log.emit(
                            "Inference: memuat model 'yolov5n' via ultralytics (fallback)"
                        )
                    except Exception as e:
                        self.log.emit(f"Inference: gagal memuat model: {e}")
                        self.model = None

            if self.model is None:
                self.model_ready.emit(False)
                return

            self.model_ready.emit(True)
        except Exception as e:
            self.log.emit(f"Inference: error saat inisialisasi model: {e}")
            self.model_ready.emit(False)
            return

        self._running = True
        while self._running:
            if not self._queue:
                time.sleep(0.01)
                continue

            frame = self._queue.pop(0)
            if frame is None:
                continue

            try:
                results = None
                try:
                    results = self.model(frame, imgsz=self.imgsz, conf=self.conf)
                except TypeError:
                    results = self.model.predict(
                        source=frame, imgsz=self.imgsz, conf=self.conf
                    )

                if not results:
                    self.frame_processed.emit(frame)
                    continue

                res = results[0] if isinstance(results, (list, tuple)) else results

                boxes = []
                labels = []
                scores = []
                try:
                    for b in getattr(res, "boxes", []):
                        x1, y1, x2, y2 = b.xyxy.tolist()[0]
                        conf_score = (
                            float(b.conf.tolist()[0])
                            if hasattr(b, "conf")
                            else (float(b.conf) if hasattr(b, "conf") else 0.0)
                        )
                        cls = (
                            int(b.cls.tolist()[0])
                            if hasattr(b, "cls")
                            else (int(b.cls) if hasattr(b, "cls") else -1)
                        )
                        name = (
                            res.names[int(cls)]
                            if hasattr(res, "names") and cls >= 0
                            else str(cls)
                        )
                        boxes.append((x1, y1, x2, y2))
                        labels.append(name)
                        scores.append(conf_score)
                except Exception:
                    try:
                        # fallback parsing (old API)
                        for box in res.boxes.xyxy:
                            x1, y1, x2, y2 = box.tolist()
                            boxes.append((x1, y1, x2, y2))
                        for conf in res.boxes.conf:
                            scores.append(float(conf))
                        for cls in res.boxes.cls:
                            cls_i = int(cls)
                            labels.append(
                                res.names[cls_i]
                                if hasattr(res, "names")
                                else str(cls_i)
                            )
                    except Exception:
                        pass

                from core.utils import draw_boxes_on_frame

                out = draw_boxes_on_frame(frame, boxes, labels, scores)
                self.frame_processed.emit(out)
            except Exception as e:
                self.log.emit(f"Inference: exception saat memproses frame: {e}")
        self.log.emit("Inference: worker berhenti")

    @pyqtSlot(object)
    def submit_frame(self, frame):
        if frame is None:
            return
        self._queue.append(frame)

    def stop(self):
        self._running = False
        self.wait(timeout=2000)

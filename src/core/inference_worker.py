import time
from collections import deque
import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from ultralytics import YOLO
from core.utils import draw_boxes_on_frame
from configs import config
from controllers.serial_controller import SerialController


class InferenceWorker(QThread):
    """Worker thread responsible for YOLO inference on frames from two cameras."""

    # -----------------------------
    # SIGNALS
    # -----------------------------
    frame_processed = pyqtSignal(tuple)  # Emits (side, processed_frame)
    log = pyqtSignal(str)

    # -----------------------------
    # INITIALIZATION
    # -----------------------------
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model_path = config.YOLO_MODEL_PATH
        self.imgsz = config.YOLO_IMAGE_SIZE
        self.conf = config.YOLO_CONFIDENCE
        self.running = False

        # Separate frame queues for left and right cameras
        self.frame_queue = {
            "left": deque(maxlen=config.QUEUE_MAXLEN),
            "right": deque(maxlen=config.QUEUE_MAXLEN),
        }

        # Track which camera should be processed next (for round-robin scheduling)
        self.last_side = "right"

        self.model = None

        self.serial = SerialController(
            port=config.SERIAL_PORT, baudrate=config.SERIAL_BAUDRATE
        )

    # -----------------------------
    # THREAD LIFECYCLE
    # -----------------------------
    def run(self):
        """Main thread loop: perform YOLO inference in a round-robin manner."""
        self.running = True
        self._load_model()

        while self.running:
            side = self._get_next_camera_side()

            # Get next frame if available
            frame = self._pop_frame(side)
            if frame is not None:
                self._process_frame(side, frame)
                self.last_side = side
            else:
                # Sleep briefly if no new frames are available
                time.sleep(0.01)

    def stop(self):
        """Stop the inference thread gracefully."""
        self.running = False
        self.wait()

    # -----------------------------
    # FRAME HANDLING
    # -----------------------------
    def submit_frame(self, data):
        """Receive frame from main thread: (side, frame)."""
        if not self.running:
            return

        side, frame = data
        if side in self.frame_queue:
            self.frame_queue[side].append(frame)

    def _get_next_camera_side(self):
        """Round-robin scheduler: alternate between left and right cameras."""
        return "left" if self.last_side == "right" else "right"

    def _pop_frame(self, side):
        """Retrieve the next available frame from queues."""
        if self.frame_queue[side]:
            return self.frame_queue[side].popleft()

        alt_side = "left" if side == "right" else "right"
        if self.frame_queue[alt_side]:
            return self.frame_queue[alt_side].popleft()

        return None

    # -----------------------------
    # YOLO INFERENCE
    # -----------------------------
    def _load_model(self):
        """Load YOLO model from the given path, fallback to default if failed."""
        try:
            self.log.emit(f"[Inference] Loading model from: {self.model_path}")
            self.model = YOLO(self.model_path)
            self.log.emit(f"[Inference] Model '{self.model_path}' loaded successfully.")

        except Exception as e:
            self.log.emit(f"[Inference] Failed to load local model: {e}")
            self._load_fallback_model()

    def _load_fallback_model(self):
        """Try to load fallback YOLO model if main model fails."""
        fallback = "yolov8n.pt"
        try:
            self.log.emit(f"[Inference] Trying fallback model '{fallback}'...")
            self.model = YOLO(fallback)
            self.log.emit(
                f"[Inference] Fallback model '{fallback}' loaded successfully."
            )
        except Exception as e2:
            self.log.emit(f"[Inference] Failed to load fallback model: {e2}")
            self.running = False

    def _process_frame(self, side, frame):
        """Run YOLO inference on a single frame."""
        if self.model is None:
            return

        try:
            # Perform inference
            results = self.model.predict(
                source=frame,
                imgsz=self.imgsz,
                conf=self.conf,
                verbose=False,
            )

            # Extract detection data
            result = results[0]
            boxes, labels, confs = self._extract_detections(result)

            # Draw detection boxes
            frame_out = draw_boxes_on_frame(frame, boxes, labels, confs)

            # Emit result to GUI
            self.frame_processed.emit((side, frame_out))

            # Send to Arduino if any object detected
            if len(boxes) > 0:
                side_msg = "LEFT_DETECTED" if side == "left" else "RIGHT_DETECTED"
                self.serial.send_message(side_msg)
                self.log.emit(f"[SERIAL-{self.serial.read_message()}")

            # Log detection info
            self.log.emit(f"[Inference-{side}] {len(boxes)} objects detected.")
        except Exception as e:
            self.log.emit(f"[Inference-{side}] Error: {e}")

    def _extract_detections(self, result):
        """Extract bounding boxes, class labels, and confidences from YOLO result."""
        if len(result.boxes) == 0:
            return [], [], []

        boxes = result.boxes.xyxy.cpu().numpy()
        labels = [result.names[int(cls)] for cls in result.boxes.cls.cpu().numpy()]
        confs = result.boxes.conf.cpu().numpy()

        return boxes, labels, confs

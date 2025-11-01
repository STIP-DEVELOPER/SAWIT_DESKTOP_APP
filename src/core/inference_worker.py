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
    """
    Handles YOLO object detection and serial communication to Arduino.
    Includes frame queueing, frame skipping, and object position logic.
    """

    frame_processed = pyqtSignal(object)
    log = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model_path = config.YOLO_MODEL_PATH
        self.imgsz = config.YOLO_IMAGE_SIZE
        self.conf = config.YOLO_CONFIDENCE
        self.running = False
        self.frame_queue = deque(maxlen=config.QUEUE_MAXLEN)
        self.model = None
        self._frame_counter = 0

        # Initialize Serial Controller
        self.serial = SerialController(
            port=config.SERIAL_PORT, baudrate=config.SERIAL_BAUDRATE
        )

    def run(self):
        """Main thread loop for inference processing."""
        self.running = True
        self._load_model()

        while self.running:
            if not self.frame_queue:
                time.sleep(0.01)
                continue

            frame = self.frame_queue.popleft()
            self._process_frame(frame)

    def stop(self):
        """Stops inference thread and closes resources."""
        self.running = False
        self.wait()

    def submit_frame(self, frame):
        """Adds a new frame to the processing queue."""
        if self.running:
            self.frame_queue.append(frame)

    def _load_model(self):
        """Loads YOLO model for object detection."""
        try:
            self.log.emit(f"[Inference] Loading model: {self.model_path}")
            self.model = YOLO(self.model_path)
            self.log.emit("[Inference] Model loaded successfully.")
        except Exception as e:
            self.log.emit(f"[Inference] Failed to load model: {e}")
            # Fallback to default lightweight YOLO model
            self.model = YOLO("yolov8n.pt")

    def _process_frame(self, frame):
        """Processes a single video frame for object detection."""
        if self.model is None:
            return

        try:
            # Frame skipping → only detect every 3 frames
            self._frame_counter += 1
            if self._frame_counter % config.YOLO_FRAME_SKIP != 0:
                return

            results = self.model.predict(
                source=frame, imgsz=self.imgsz, conf=self.conf, verbose=False
            )

            result = results[0]
            boxes, labels, confs = self._extract_detections(result)
            frame_out = draw_boxes_on_frame(frame, boxes, labels, confs)

            if len(boxes) > 0:
                frame_width = frame.shape[1]

                for box in boxes:
                    x1, y1, x2, y2 = map(int, box)
                    x_center = (x1 + x2) / 2

                    position = self._get_object_position(x_center, frame_width)

                    # Decide message based on position
                    if position == "LEFT":
                        message = "LEFT_DETECTED"
                    elif position == "CENTER":
                        message = "CENTER_DETECTED"
                    else:
                        message = "RIGHT_DETECTED"

                    # Send message to Arduino
                    self.serial.send_message(message)
                    self.log.emit(f"[Detection] {message}")

            # Emit processed frame to UI
            self.frame_processed.emit(frame_out)

        except Exception as e:
            self.log.emit(f"[Inference] Error: {e}")

    def _get_object_position(self, x_center, frame_width, tolerance=0.2):
        """
        Determines object position (LEFT, CENTER, RIGHT) based on bounding box center.
        tolerance defines how wide the center zone is (e.g., 0.2 = 20% of frame width).
        """
        left_threshold = frame_width * (0.5 - tolerance)
        right_threshold = frame_width * (0.5 + tolerance)

        if x_center < left_threshold:
            return "LEFT"
        elif x_center > right_threshold:
            return "RIGHT"
        else:
            return "CENTER"

    def _extract_detections(self, result):
        """Extracts bounding boxes, labels, and confidence scores from YOLO output."""
        if len(result.boxes) == 0:
            return [], [], []

        boxes = result.boxes.xyxy.cpu().numpy()
        labels = [result.names[int(cls)] for cls in result.boxes.cls.cpu().numpy()]
        confs = result.boxes.conf.cpu().numpy()
        return boxes, labels, confs

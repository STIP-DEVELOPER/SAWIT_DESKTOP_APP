import sys
import os
import time
from collections import deque
import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from core.logger import add_log
from core.utils import draw_boxes_on_frame
from configs import config
from controllers.serial_controller import SerialController

sys.path.append(os.path.join(os.getcwd(), "yolov5"))
from models.common import DetectMultiBackend
from utils.torch_utils import select_device
from utils.general import non_max_suppression, scale_boxes
from utils.augmentations import letterbox
import torch


class InferenceWorker(QThread):
    """
    Handles YOLOv5 object detection and serial communication with Arduino.
    Includes frame queueing, frame skipping, and object position determination.
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
        self.device = select_device('')
        self._frame_counter = 0
        self.serial = SerialController(port=config.SERIAL_PORT, baudrate=config.SERIAL_BAUDRATE)

    def run(self):
        """Main loop for inference."""
        self.running = True
        self._load_model()

        while self.running:
            if not self.frame_queue:
                time.sleep(0.01)
                # time.sleep(5.2)
                continue

            frame = self.frame_queue.popleft()
            self._process_frame(frame)

    def stop(self):
        """Stop the inference thread safely."""
        self.running = False
        self.wait()

    def submit_frame(self, frame):
        """Add a new frame to the processing queue."""
        if self.running:
            self.frame_queue.append(frame)

    def load_new_model(self, new_model_path):
        """Reload YOLOv5 model during runtime."""
        try:
            self.log.emit(f"[Inference] Loading new model: {new_model_path}")
            self.model_path = new_model_path
            self._load_model()
            self.log.emit(f"[Inference] Model switched successfully → {new_model_path}")
        except Exception as e:
            self.log.emit(f"[Inference] Failed to switch model: {e}")
            add_log("ERROR", "InferenceWorker", f"Failed to switch model: {e}")

    def _load_model(self):
        """Load YOLOv5 model using DetectMultiBackend."""
        try:
            self.log.emit(f"[Inference] Loading YOLOv5 model: {self.model_path}")
            self.model = DetectMultiBackend(self.model_path, device=self.device)
            self.log.emit("[Inference] YOLOv5 model loaded successfully.")
        except Exception as e:
            self.log.emit(f"[Inference] Failed to load model: {e}")
            add_log("ERROR", "InferenceWorker", f"Failed to load model: {e}")

    def _process_frame(self, frame):
        """Run YOLOv5 detection on a single frame."""
        if self.model is None:
            return

        try:
            self._frame_counter += 1
            if self._frame_counter % config.YOLO_FRAME_SKIP != 0:
                return

            boxes, labels, confs = self._predict_v5(frame)
            frame_out = draw_boxes_on_frame(frame, boxes, labels, confs)

            if len(boxes) > 0:
                frame_width = frame.shape[1]
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box)
                    x_center = (x1 + x2) / 2
                    position = self._get_object_position(x_center, frame_width)

                    message = f"{position}_DETECTED"
                    self.serial.send_message(message)
                    self.log.emit(f"[Detection] {message}")

            self.frame_processed.emit(frame_out)

        except Exception as e:
            self.log.emit(f"[Inference] Error: {e}")
            add_log("ERROR", "InferenceWorker", f"Inference error: {e}")

    def _predict_v5(self, frame):
        """Run YOLOv5 inference manually."""
        img = letterbox(frame, self.imgsz, stride=self.model.stride, auto=True)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        im = torch.from_numpy(img).to(self.device)
        im = im.float() / 255.0
        if len(im.shape) == 3:
            im = im[None]

        pred = self.model(im, augment=False, visualize=False)
        pred = non_max_suppression(pred, self.conf, 0.45, max_det=1000)
        boxes, labels, confs = [], [], []

        for det in pred:
            if len(det):
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], frame.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    boxes.append(xyxy)
                    confs.append(float(conf))
                    labels.append(self.model.names[int(cls)])

        return np.array(boxes), labels, confs

    def _get_object_position(self, x_center, frame_width, tolerance=0.1):
        """Determine object position: LEFT, CENTER, or RIGHT. The CENTER zone is now smaller (tolerance < 0.1) or 10%, so objects in the middle are less likely to be classified as CENTER. """
        
        left_threshold = frame_width * (0.5 - tolerance)
        right_threshold = frame_width * (0.5 + tolerance)

        if x_center < left_threshold:
            return "LEFT"
        elif x_center > right_threshold:
            return "RIGHT"
        else:
            return "CENTER"

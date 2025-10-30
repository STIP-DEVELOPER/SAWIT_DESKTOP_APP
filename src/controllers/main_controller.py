from core.camera_capture import CameraCapture
from core.inference_worker import InferenceWorker
from core.utils import convert_frame_to_qpixmap
from configs import config


class MainController:
    """Manages camera threads, inference, and UI updates."""

    def __init__(self, ui):
        self.ui = ui
        self._setup_components()
        self._connect_signals()
        self.latest_left_frame = None
        self.latest_right_frame = None

    # --------------------------------------------------
    # Initialization
    # --------------------------------------------------
    def _setup_components(self):
        self.left_camera = CameraCapture(config.LEFT_CAMERA_INDEX, name="left")
        self.right_camera = CameraCapture(config.RIGHT_CAMERA_INDEX, name="right")
        self.inference_worker = InferenceWorker(
            model_path=config.YOLO_MODEL_PATH,
            imgsz=config.YOLO_IMAGE_SIZE,
            conf=config.YOLO_CONFIDENCE,
        )

    def _connect_signals(self):
        # Camera → Frame Handler
        self.left_camera.frame_ready.connect(self._on_left_frame)
        self.right_camera.frame_ready.connect(self._on_right_frame)

        # Worker → Processed Frame & Log
        self.inference_worker.frame_processed.connect(self._on_inference_result)
        self.inference_worker.log.connect(self._append_log)

        # UI → Buttons
        self.ui.start_button.clicked.connect(self.start)
        self.ui.stop_button.clicked.connect(self.stop)
        self.ui.exit_button.clicked.connect(self._exit_app)

    # --------------------------------------------------
    # Camera Control
    # --------------------------------------------------
    def start(self):
        self._append_log(f"{config.LOG_PREFIX_SYSTEM} Starting cameras...")
        self.inference_worker.start()
        self.left_camera.start()
        self.right_camera.start()

    def stop(self):
        self._append_log(f"{config.LOG_PREFIX_SYSTEM} Stopping cameras...")
        self.left_camera.stop()
        self.right_camera.stop()
        self.inference_worker.stop()

    def _exit_app(self):
        self.stop()
        self.ui.close()

    # --------------------------------------------------
    # Frame Handlers
    # --------------------------------------------------
    def _on_left_frame(self, frame):
        self.latest_left_frame = frame
        if frame is not None:
            self._update_view(self.ui.left_label, frame)
            self.inference_worker.submit_frame(("left", frame))

    def _on_right_frame(self, frame):
        self.latest_right_frame = frame
        if frame is not None:
            self._update_view(self.ui.right_label, frame)
            self.inference_worker.submit_frame(("right", frame))

    def _on_inference_result(self, result):
        if not isinstance(result, tuple) or len(result) != 2:
            return
        side, frame = result
        target_label = self.ui.left_label if side == "left" else self.ui.right_label
        self._update_view(target_label, frame)

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------
    def _update_view(self, label, frame):
        pixmap = convert_frame_to_qpixmap(frame)
        label.setPixmap(pixmap)

    def _append_log(self, text):
        self.ui.log_box.append(text)

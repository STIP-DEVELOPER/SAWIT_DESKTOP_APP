from core.camera_capture import CameraCapture
from core.inference_worker import InferenceWorker
from core.logger import add_log
from core.utils import convert_frame_to_qpixmap
from configs import config
from core.video_capture import VideoCaptureThread  # new


class MainController:
    """Manages single camera, inference, and UI updates."""

    def __init__(self, ui):
        self.ui = ui
        self._setup_components()
        self._connect_signals()
        self.latest_frame = None

    def _setup_components(self):
        # self.camera = CameraCapture(config.CAMERA_INDEX, name="center")
        self.camera = VideoCaptureThread(
            "videos/test2.mp4", name="center"
        )  # video file
        self.inference_worker = InferenceWorker()

    def _connect_signals(self):
        self.camera.frame_ready.connect(self._on_frame)
        self.inference_worker.frame_processed.connect(self._on_inference_result)
        self.inference_worker.log.connect(self._append_log)

        self.ui.start_button.clicked.connect(self.start)
        self.ui.stop_button.clicked.connect(self.stop)
        self.ui.exit_button.clicked.connect(self._exit_app)
        self.ui.toggle_camera_button.clicked.connect(self._toggle_camera_view)

    def start(self):
        self._append_log("[System] Starting camera...")
        selected_model = config.YOLO_MODEL_PATH

        if "Small-Tree" in selected_model:
            model_path = config.YOLO_MODEL_SMALL
        elif "Medium-Tree" in selected_model:
            model_path = config.YOLO_MODEL_MEDIUM
        else:
            model_path = config.YOLO_MODEL_LARGE

        # Set model path before starting inference
        self.inference_worker.model_path = model_path
        self._append_log(f"[Model] Selected model: {selected_model} ({model_path})")
        self.inference_worker.start()
        self.camera.start()
        add_log(
            "INFO", "System", f"[Model] Selected model: {selected_model} ({model_path})"
        )

    def stop(self):
        self._append_log("[System] Stopping camera...")
        self.camera.stop()
        self.inference_worker.stop()

    def _exit_app(self):
        self.stop()
        self.ui.close()

    def _on_frame(self, frame):
        self.latest_frame = frame
        if frame is not None:
            # Only render to UI if camera view is shown
            if self.ui.show_camera:
                self._update_view(self.ui.camera_label, frame)
            # Still process frame for inference even if camera is hidden
            self.inference_worker.submit_frame(frame)

    def _on_inference_result(self, frame):
        if self.ui.show_camera:
            self._update_view(self.ui.camera_label, frame)

    def _update_view(self, label, frame):
        pixmap = convert_frame_to_qpixmap(frame)
        label.setPixmap(pixmap)

    def _append_log(self, text):
        self.ui.log_box.append(text)

    def _toggle_camera_view(self):
        """Toggle visibility of camera display, without stopping detection."""
        self.ui.show_camera = not self.ui.show_camera

        if self.ui.show_camera:
            self.ui.camera_label.show()
            self.ui.toggle_camera_button.setText("Hide Camera")
            self._append_log("[UI] Camera view enabled.")
        else:
            self.ui.camera_label.hide()
            self.ui.toggle_camera_button.setText("Show Camera")
            self._append_log("[UI] Camera view hidden.")

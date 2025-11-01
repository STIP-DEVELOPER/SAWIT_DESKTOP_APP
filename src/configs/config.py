# ============================================================
# MAIN CONFIGURATION
# ============================================================

# ------------------------------------------------------------
# YOLO MODEL CONFIGURATION
# ------------------------------------------------------------
YOLO_MODEL_PATH = "models/yolov5n.pt"  # Path to the YOLO model file
YOLO_IMAGE_SIZE = 320  # Input image size for YOLO inference
YOLO_CONFIDENCE = 0.4  # Minimum confidence threshold for detection
YOLO_FRAME_SKIP = 5  # TOTAL_FRAME / YOLO_FRAME_SKIP = reduced FPS for inference

# ------------------------------------------------------------
# CAMERA CONFIGURATION
# ------------------------------------------------------------
LEFT_CAMERA_INDEX = 0  # Index of the left camera (only for multi-camera setups)
RIGHT_CAMERA_INDEX = 1  # Index of the right camera (only for multi-camera setups)
CAMERA_INDEX = 0  # single center camera
SHOW_CAMERA_DEFAULT = True

CAMERA_BACKEND = 0  # 0 = Default OpenCV backend (use cv2.CAP_ANY)
FRAME_DELAY = 0.05  # Delay between frames to limit FPS (~30 FPS)
QUEUE_MAXLEN = 2  # Maximum queue size per camera (for frame buffering)

# ------------------------------------------------------------
# USER INTERFACE CONFIGURATION
# ------------------------------------------------------------
WINDOW_TITLE = "SAWIT APP"
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 360

# ------------------------------------------------------------
# LOGGING CONFIGURATION
# ------------------------------------------------------------
LOG_PREFIX_SYSTEM = "[System]"
LOG_PREFIX_CAMERA = "[Camera]"
LOG_PREFIX_INFERENCE = "[Inference]"

# ------------------------------------------------------------
# SERIAL CONFIG
# ------------------------------------------------------------
SERIAL_PORT = "/dev/tty.usbserial-1410"  # Update this to your Arduino port
SERIAL_BAUDRATE = 9600

# ------------------------------------------------------------
# MISC / DEVELOPMENT SETTINGS
# ------------------------------------------------------------
DEBUG_MODE = True  # Enable verbose logging or additional debug output

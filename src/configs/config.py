# ============================================================
# MAIN CONFIGURATION
# ============================================================

# ------------------------------------------------------------
# YOLO MODEL CONFIGURATION
# ------------------------------------------------------------
YOLO_MODEL_PATH = "models/yolov5n.pt"  # Path to the YOLO model file
YOLO_IMAGE_SIZE = 320  # Input image size for YOLO inference
YOLO_CONFIDENCE = 0.4  # Minimum confidence threshold for detection

# ------------------------------------------------------------
# CAMERA CONFIGURATION
# ------------------------------------------------------------
LEFT_CAMERA_INDEX = 0  # Index of the left camera
RIGHT_CAMERA_INDEX = 1  # Index of the right camera
CAMERA_BACKEND = 0  # 0 = Default OpenCV backend (use cv2.CAP_ANY)
FRAME_DELAY = 0.03  # Delay between frames to limit FPS (~30 FPS)
QUEUE_MAXLEN = 2  # Maximum queue size per camera (for frame buffering)

# ------------------------------------------------------------
# USER INTERFACE CONFIGURATION
# ------------------------------------------------------------
WINDOW_TITLE = "SAWIT APP"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# ------------------------------------------------------------
# LOGGING CONFIGURATION
# ------------------------------------------------------------
LOG_PREFIX_SYSTEM = "[System]"
LOG_PREFIX_CAMERA = "[Camera]"
LOG_PREFIX_INFERENCE = "[Inference]"

# ------------------------------------------------------------
# MISC / DEVELOPMENT SETTINGS
# ------------------------------------------------------------
DEBUG_MODE = True  # Enable verbose logging or additional debug output

import os
import json

from core.logger import add_log

# ------------------------------------------------------------
# YOLO MODEL CONFIGURATION
# ------------------------------------------------------------
YOLO_MODEL_PATH = "models/medium-v2.pt"  # Path to the YOLO model file

YOLO_MODEL_SMALL = "models/medium-v2.pt"
YOLO_MODEL_MEDIUM = "models/medium-v2.pt"
YOLO_MODEL_LARGE = "models/medium-v2.pt"


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
FRAME_DELAY = 0.03  # Delay between frames to limit FPS (~30 FPS)
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

MAX_LOG_COUNT = 2

# ------------------------------------------------------------
# SERIAL CONFIG
# ------------------------------------------------------------
SERIAL_PORT = "/dev/tty.usbserial-1410"  # Update this to your Arduino port
SERIAL_BAUDRATE = 9600

# ------------------------------------------------------------
# MISC / DEVELOPMENT SETTINGS
# ------------------------------------------------------------
DEBUG_MODE = True  # Enable verbose logging or additional debug output


# ============================================================
# LOAD SETTINGS FROM JSON
# ============================================================

SETTINGS_FILE = os.path.join(os.getcwd(), "settings.json")


if os.path.exists(SETTINGS_FILE):
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)

        # Update konfigurasi dari file JSON
        YOLO_MODEL = settings.get("YOLO_MODEL", None)
        YOLO_MODEL_PATH = settings.get("MODEL_PATH", YOLO_MODEL_PATH)
        CAMERA_INDEX = settings.get("CAMERA_INDEX", CAMERA_INDEX)
        YOLO_IMAGE_SIZE = settings.get("YOLO_IMAGE_SIZE", YOLO_IMAGE_SIZE)
        YOLO_CONFIDENCE = settings.get("YOLO_CONFIDENCE", YOLO_CONFIDENCE)
        YOLO_FRAME_SKIP = settings.get("YOLO_FRAME_SKIP", YOLO_FRAME_SKIP)
        SERIAL_PORT = settings.get("SERIAL_PORT", SERIAL_PORT)
        SERIAL_BAUDRATE = settings.get("SERIAL_BAUDRATE", SERIAL_BAUDRATE)

        # Optional log info saat DEBUG_MODE aktif
        if DEBUG_MODE:
            print(f"[CONFIG] Loaded settings from {SETTINGS_FILE}")
            print(f"[CONFIG] Model Path: {YOLO_MODEL_PATH}")
            print(f"[CONFIG] Camera Index: {CAMERA_INDEX}")
            print(f"[CONFIG] Confidence: {YOLO_CONFIDENCE}")
            print(f"[CONFIG] Frame Skip: {YOLO_FRAME_SKIP}")
            print(f"[CONFIG] Serial Port: {SERIAL_PORT}")

    except Exception as e:
        add_log("ERROR", "Config", f"Failed to load settings.json: {e}")
else:
    if DEBUG_MODE:
        add_log(
            "WARNING", "Config", "settings.json not found, using default configuration."
        )

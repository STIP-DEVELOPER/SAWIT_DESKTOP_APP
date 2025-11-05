import torch
from yolov5 import detect

# Jalankan deteksi langsung dari YOLOv5 script
# Pastikan path model dan video benar
detect.run(
    weights="test/medium-v2.pt",  # model hasil training YOLOv5
    source="test/video-1.MOV",    # file video kamu
    conf_thres=0.4,               # confidence threshold
    imgsz=640,                    # resolusi input
    project="runs/detect",        # folder output
    name="video-test",            # nama subfolder output
    exist_ok=True                 # overwrite jika sudah ada
)

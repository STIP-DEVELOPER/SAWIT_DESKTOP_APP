from PyQt5.QtGui import QImage, QPixmap
import numpy as np
import cv2


def frame_to_qpixmap(frame: np.ndarray):
    if frame is None:
        return QPixmap()

    if len(frame.shape) == 2:
        h, w = frame.shape
        bytes_per_line = w
        qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
    else:
        bgr = frame
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(qimg)


def draw_boxes_on_frame(frame, boxes, labels, scores):
    import cv2

    out = frame.copy()
    for (x1, y1, x2, y2), label, score in zip(boxes, labels, scores):
        cv2.rectangle(out, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        text = f"{label} {score:.2f}"
        cv2.putText(
            out,
            text,
            (int(x1), int(y1) - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )
    return out

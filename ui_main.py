from core.serial_handler import SerialReader
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QGridLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from core.yolo_detector import YoloDetector


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Pemupuk Otomatis Sawit")
        self.setGeometry(100, 100, 1200, 700)

        # === WIDGET UTAMA ===
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # === LABEL UNTUK VIDEO FEED ===
        self.label_camera_left = QLabel("Kamera Kiri")
        self.label_camera_right = QLabel("Kamera Kanan")
        self.label_camera_left.setAlignment(Qt.AlignCenter)
        self.label_camera_right.setAlignment(Qt.AlignCenter)
        self.label_camera_left.setStyleSheet("background-color: #2c3e50; color: white;")
        self.label_camera_right.setStyleSheet(
            "background-color: #2c3e50; color: white;"
        )

        # === LABEL UNTUK DATA JARAK ===
        self.label_distance = QLabel("Jarak: -")
        self.label_distance.setAlignment(Qt.AlignCenter)
        self.label_distance.setStyleSheet(
            "font-size: 18px; color: #2c3e50; padding: 8px;"
        )

        self.label_motor_auto = QLabel("Motor Otomatis: OFF")
        self.label_motor_auto.setAlignment(Qt.AlignCenter)
        self.label_motor_auto.setStyleSheet(
            "font-size: 18px; padding: 10px; background-color: #c0392b; color: white;"
        )

        # === LOG PANEL ===
        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)

        # === BUTTON CONTROL ===
        self.btn_manual_on = QPushButton("🔆 Aktifkan Motor")
        self.btn_manual_off = QPushButton("💤 Matikan Motor")

        # === LAYOUT SETUP ===
        layout = QGridLayout()
        layout.addWidget(self.label_camera_left, 0, 0)
        layout.addWidget(self.label_camera_right, 0, 1)

        layout.addWidget(self.label_distance, 1, 0, 1, 2)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_manual_on)
        button_layout.addWidget(self.btn_manual_off)
        layout.addLayout(button_layout, 2, 0, 1, 2)

        layout.addWidget(QLabel("Log Aktivitas:"), 3, 0, 1, 2)
        layout.addWidget(self.text_log, 4, 0, 1, 2)
        layout.addWidget(self.label_motor_auto, 2, 0, 1, 2)

        central_widget.setLayout(layout)

        # === INISIASI KAMERA & SERIAL ===
        self.init_cameras()
        self.init_serial()

    def init_cameras(self):
        # Kamera kiri
        self.camera_left = YoloDetector(0)
        self.camera_left.frame_update.connect(
            lambda img: self.label_camera_left.setPixmap(QPixmap.fromImage(img))
        )
        self.camera_left.detection_update.connect(self.check_motor_auto)
        self.camera_left.start()

        # Kamera kanan
        self.camera_right = YoloDetector(1)
        self.camera_right.frame_update.connect(
            lambda img: self.label_camera_right.setPixmap(QPixmap.fromImage(img))
        )
        self.camera_right.detection_update.connect(self.check_motor_auto)
        self.camera_right.start()

    def init_serial(self):
        self.serial_thread = SerialReader()
        self.serial_thread.data_received.connect(self.update_distance)
        self.serial_thread.start()

    def update_frame(self, image, camera_name):
        if camera_name == "left":
            self.label_camera_left.setPixmap(QPixmap.fromImage(image))
        elif camera_name == "right":
            self.label_camera_right.setPixmap(QPixmap.fromImage(image))

        self.text_log.append(f"🖼 {camera_name} frame diperbarui")

    def update_distance(self, distance_str):
        """Perbarui label jarak dan log"""
        try:
            distance = float(distance_str)
            self.label_distance.setText(f"Jarak: {distance:.2f} meter")
            self.text_log.append(f"📏 {distance:.2f} m diterima")
        except ValueError:
            print(f"Data tidak valid: {distance_str}")

    # --- METHOD UNTUK MEMERIKSA MOTOR OTOMATIS ---
    def check_motor_auto(self, side_detected):
        """Aktifkan motor otomatis jika jarak < 2m dan ada sawit terdeteksi"""
        try:
            distance_text = (
                self.label_distance.text().replace("Jarak: ", "").replace(" meter", "")
            )
            distance = float(distance_text)
            if distance < 2.0:
                self.label_motor_auto.setText(f"Motor Otomatis: ON ({side_detected})")
                self.label_motor_auto.setStyleSheet(
                    "font-size: 18px; padding: 10px; background-color: #27ae60; color: white;"
                )
                self.text_log.append(
                    f"⚡ Motor otomatis ON karena {side_detected}, jarak {distance:.2f} m"
                )
            else:
                self.label_motor_auto.setText("Motor Otomatis: OFF")
                self.label_motor_auto.setStyleSheet(
                    "font-size: 18px; padding: 10px; background-color: #c0392b; color: white;"
                )
        except ValueError:
            pass

    def closeEvent(self, event):
        self.camera_left.stop()
        self.camera_right.stop()
        self.serial_thread.stop()
        event.accept()

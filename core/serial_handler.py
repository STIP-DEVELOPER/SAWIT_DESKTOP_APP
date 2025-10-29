import serial
import serial.tools.list_ports
from PyQt5.QtCore import QThread, pyqtSignal


class SerialReader(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port=None, baudrate=9600):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.running = False

    def find_arduino_port(self):
        """Cari port Arduino secara otomatis"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if (
                "Arduino" in port.description
                or "usbmodem" in port.device
                or "usbserial" in port.device
            ):
                return port.device
        return None

    def run(self):
        if self.port is None:
            self.port = self.find_arduino_port()

        if self.port is None:
            print("❌ Arduino tidak ditemukan.")
            return

        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self.running = True
            print(f"✅ Terhubung ke Arduino di {self.port}")
        except Exception as e:
            print(f"⚠️ Gagal membuka port: {e}")
            return

        while self.running:
            try:
                line = self.ser.readline().decode("utf-8").strip()
                if line:
                    self.data_received.emit(line)
            except Exception as e:
                print(f"⚠️ Error baca serial: {e}")
                self.running = False

        self.ser.close()

    def stop(self):
        self.running = False
        self.wait()

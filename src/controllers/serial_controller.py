import serial
import threading
import time
import queue
from configs import config
from core.logger import add_log
from PyQt5.QtCore import QThread, pyqtSignal



class SerialController(QThread):
    """
    Handles serial communication with Arduino.
    - Queue-based sender (no thread flood)
    - Background read loop to track Arduino status
    - Safe from flooding (rate limiting)
    """
    log = pyqtSignal(str)

    def __init__(
        self,
        port: str = config.SERIAL_PORT,
        baudrate: int = config.SERIAL_BAUDRATE,
        min_interval: float = 0.5,  # minimum interval between messages (seconds)
        parent=None
    ):
        super().__init__(parent)
        self.port = port
        self.baudrate = baudrate
        self.lock = threading.Lock()
        self.ser = None
        self.status = "UNKNOWN"  # "READY", "BUSY", or "UNKNOWN"
        self._running = True
        self._last_send_time = 0
        self.min_interval = min_interval

        # Queue for outgoing messages
        self._send_queue = queue.Queue()

        # Connect to Arduino
        self._connect()

        # Thread pembaca serial (mendengar status dari Arduino)
        self._reader_thread = threading.Thread(target=self._read_loop, daemon=True)
        self._reader_thread.start()

        # Thread pengirim serial (ambil dari queue dan kirim satu per satu)
        self._sender_thread = threading.Thread(target=self._send_worker, daemon=True)
        self._sender_thread.start()

    # --------------------------------------------------
    # CONNECTION
    # --------------------------------------------------
    def _connect(self):
        """Try to connect to the Arduino via serial port."""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            
            self.log.emit(
                    f"[SERIAL]-Connected to {self.port} at {self.baudrate} baud."
                )
            
            add_log(
                "INFO",
                "SerialController",
                f"Connected to {self.port} at {self.baudrate} baud.",
            )
        except Exception as e:
            self.log.emit(f"[SERIAL]-Failed to connect to {self.port}: {e}")
            add_log(
                "ERROR", "SerialController", f"Failed to connect to {self.port}: {e}"
            )
            self.ser = None

    # --------------------------------------------------
    # SENDER
    # --------------------------------------------------
    def send_message(self, message: str):
        """
        Kirim pesan ke Arduino melalui queue.
        Pesan akan dikirim oleh _send_worker agar tidak membuat banyak thread.
        """
        now = time.time()

        if now - self._last_send_time < self.min_interval:
            self.log.emit(f"[SERIAL]-Too soon since last send — throttling.")

            return

        if self.status != "READY":
            self.log.emit(f"[SERIAL]-MCU is {self.status}. Command skipped.")
            return

        self._last_send_time = now
        self._send_queue.put(message)

    def _send_worker(self):
        """Worker thread untuk mengirim pesan dari queue ke Arduino."""
        while self._running:
            try:
                message = self._send_queue.get(timeout=0.1)
                if not self.ser or not self.ser.is_open:
                    continue

                with self.lock:
                    self.ser.write(f"{message}\n".encode())
                    self.ser.flush()

                print(f"[Serial -> Arduino] Sent: {message}")
                self._send_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                self.log.emit(f"[SERIAL]-Send error: {e}")
                
                add_log("ERROR", "SerialController", f"Send error: {e}")
                time.sleep(0.2)

    # --------------------------------------------------
    # READER
    # --------------------------------------------------
    def _read_loop(self):
        """
        Continuously read messages from Arduino.
        Expected messages: "BUSY", "READY", or custom feedback.
        """
        while self._running:
            try:
                if self.ser and self.ser.in_waiting:
                    line = self.ser.readline().decode(errors="ignore").strip()
                    if not line:
                        continue

                    upper = line.upper()
                    if "BUSY" in upper:
                        self.status = "BUSY"
                    elif "READY" in upper:
                        self.status = "READY"

                    print(f"[Arduino -> Python] {line}")
                    
                else:
                    time.sleep(0.05)

            except Exception as e:
                self.log.emit(f"[Serial] Read error: {e}")

                add_log("ERROR", "SerialController", f"Read error: {e}")
                time.sleep(0.5)

    # --------------------------------------------------
    # CLEANUP
    # --------------------------------------------------
    def close(self):
        """Stop threads and close the serial connection."""
        self._running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.log.emit(f"[Serial] - Serial connection closed.")

            add_log("INFO", "SerialController", "Serial connection closed.")

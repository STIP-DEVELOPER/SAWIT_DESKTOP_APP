import serial
import threading
import time
from configs import config


class SerialController:
    """
    Handles serial communication with Arduino.
    - Non-blocking write (via threads)
    - Background read loop to track Arduino status
    - Safe from flooding (rate limiting)
    """

    def __init__(
        self,
        port: str = config.SERIAL_PORT,
        baudrate: int = config.SERIAL_BAUDRATE,
        min_interval: float = 0.5,  # minimum interval between messages (seconds)
    ):
        self.port = port
        self.baudrate = baudrate
        self.lock = threading.Lock()
        self.ser = None
        self.status = "UNKNOWN"  # "READY", "BUSY", or "UNKNOWN"
        self._running = True
        self._last_send_time = 0
        self.min_interval = min_interval

        # Connect to MCU
        self._connect()

        # Start background reader thread
        self._reader_thread = threading.Thread(target=self._read_loop, daemon=True)
        self._reader_thread.start()

    def _connect(self):
        """Try to connect to the Arduino via serial port."""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"[Serial] Connected to {self.port} at {self.baudrate} baud.")
        except Exception as e:
            print(f"[Serial] Connection failed: {e}")
            self.ser = None

    def _send_thread(self, message: str):
        """Worker thread to send message safely to Arduino."""
        if not self.ser or not self.ser.is_open:
            print("[Serial] Serial port not open. Cannot send message.")
            return

        try:
            with self.lock:
                self.ser.write(f"{message}\n".encode())
                self.ser.flush()
            print(f"[Serial -> Arduino] Sent: {message}")
        except Exception as e:
            print(f"[Serial] Failed to send message: {e}")

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
                print(f"[Serial] Read error: {e}")
                time.sleep(0.5)

    def send_message(self, message: str):
        """
        Send a message to Arduino (thread-safe and rate-limited).
        Skips sending if Arduino is busy or message sent too recently.
        """
        now = time.time()

        if now - self._last_send_time < self.min_interval:
            print("[Serial] Too soon since last send — throttling.")
            return

        if self.status != "READY":
            print(f"[Serial] Arduino is {self.status}. Command skipped.")
            return

        self._last_send_time = now
        threading.Thread(target=self._send_thread, args=(message,), daemon=True).start()

    def close(self):
        """Stop threads and close the serial connection."""
        self._running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("[Serial] Connection closed.")

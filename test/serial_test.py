import serial
import time

# Konfigurasi serial (sesuaikan dengan config)
SERIAL_PORT = "/dev/tty.usbserial-1410"
BAUDRATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    print(f"[Python] Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"[Python] Failed to connect: {e}")
    exit(1)

time.sleep(2)  # Tunggu Arduino siap


def send_and_receive(msg):
    # Kirim pesan ke Arduino
    ser.write(f"{msg}\n".encode())

    # Baca balasan
    response = ser.readline().decode().strip()
    return response


# Contoh loop kirim pesan
for command in ["ON", "OFF", "ON"]:
    print(f"[Python] Sending: {command}")
    reply = send_and_receive(command)
    print(f"[Python] Arduino replied: {reply}")
    time.sleep(1)

ser.close()

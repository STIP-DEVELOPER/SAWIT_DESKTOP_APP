# setup awal

curl -LsSf https://astral.sh/uv/install.sh | sh

# buat folder dan masuk

mkdir dualcam-yolo && cd dualcam-yolo

# buat environment

uv venv

# tambahkan dependensi

uv add "numpy<2" opencv-python pyqt5 ultralytics torch pyserial

# (opsional) aktifkan venv

source .venv/bin/activate

# jalankan aplikasi

uv run python main.py

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

# common issue

## Install Python 3.10

uv python install 3.10

## Buat environment baru

uv venv --python 3.10
source .venv/bin/activate

pip install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1
pip install ultralytics==8.0.20 opencv-python

python -c "import torch; import ultralytics; print(torch.**version**)"

# setup yolov5

git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt

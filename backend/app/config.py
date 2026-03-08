import os

# MODEL_PATH = os.getenv("MODEL_PATH", "model/best_3.onnx")
# LABEL_PATH = os.getenv("LABEL_PATH", "model/label.txt")
# import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "best_3.onnx")
LABEL_PATH = os.path.join(BASE_DIR, "..", "model", "label.txt")
MODEL_W = 416
MODEL_H = 416
CONFIDENCE = 0.10
NMS_THRESHOLD = 0.40
CLOUD_NAME="dyb5z4ejf",
API_KEY=597799715354648,
API_SECRET="y7rVi2_LGkSeg_kQE0JdgsGpst8"
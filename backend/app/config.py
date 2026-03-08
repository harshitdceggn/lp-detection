import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "model", "best_3.onnx")
LABEL_PATH = os.path.join(BASE_DIR, "model", "label.txt")

MODEL_W = 416
MODEL_H = 416

CONFIDENCE = 0.10
NMS_THRESHOLD = 0.40

CLOUD_NAME = os.getenv("CLOUD_NAME")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")
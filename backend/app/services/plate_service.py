# from app.core.onnx_model import ONNXPlateModel

# _model = None

# def get_model():
#     global _model
#     if _model is None:
#         _model = ONNXPlateModel()
#     return _model

# def predict_plate(image_path):
#     model = get_model()
#     return model.predict_plate(image_path)
from app.core.model_loader import model

def predict_plate(image_path):
    return model.predict_plate(image_path)
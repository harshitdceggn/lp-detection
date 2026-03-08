import cloudinary
import cloudinary.uploader
from app.config import CLOUD_NAME, API_KEY, API_SECRET

cloudinary.config(
    cloud_name="dyb5z4ejf",
    api_key=597799715354648,
    api_secret="y7rVi2_LGkSeg_kQE0JdgsGpst8"
)

def upload_image(file_path):
    result = cloudinary.uploader.upload(file_path)
    return result["secure_url"]
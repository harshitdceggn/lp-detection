from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
from sqlalchemy.orm import Session

from app.services.plate_service import predict_plate
from app.services.cloudinary_service import upload_image
from app.database.db import SessionLocal
from app.database.models import PlateDetection

router = APIRouter()

UPLOAD_DIR = "uploads"

# create upload directory if not exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@router.post("/predict/")
async def predict(file: UploadFile = File(...)):

    try:

        # generate unique filename
        ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"

        file_path = os.path.join(UPLOAD_DIR, filename)

        # save file temporarily
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # run ML model
        plate = predict_plate(file_path)

        # upload image to cloudinary
        image_url = upload_image(file_path)

        # remove local file
        os.remove(file_path)

        # save record to database
        db: Session = SessionLocal()

        record = PlateDetection(
            plate_number=plate,
            image_path=image_url
        )

        db.add(record)
        db.commit()
        db.refresh(record)
        db.close()

        return {
            "success": True,
            "plate_number": plate,
            "image_url": image_url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
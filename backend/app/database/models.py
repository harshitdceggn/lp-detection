from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.db import Base


class PlateDetection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, index=True)
    image_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
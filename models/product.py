from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from db.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    size = Column(String, nullable=False)         
    pad_count = Column(Integer, nullable=False)
    features = Column(String, nullable=False)

    stock = Column(Integer, nullable=False)
    image_url = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

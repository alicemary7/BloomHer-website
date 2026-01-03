from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False) # e.g., "credit_card", "paypal"
    status = Column(String, default="completed")
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order")

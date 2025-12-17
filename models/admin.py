from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    # optional link to an existing user
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)
    is_super = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

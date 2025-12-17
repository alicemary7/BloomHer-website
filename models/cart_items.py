from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    variant_order = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)

    
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
    # variant relationship left out to avoid complex primaryjoin; can be added if needed
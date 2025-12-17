from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database   import Base



class Product(Base):
    __tablename__ = "products"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=False)


    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)


    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete")
    features = relationship("ProductFeature", back_populates="product", cascade="all, delete")


class ProductVariant(Base):
    __tablename__ = "product_variants"


    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))


    size = Column(String, nullable=False) 
    pads_count = Column(Integer, nullable=False) 
    stock = Column(Integer, nullable=False)
    variant_order = Column(Integer, nullable=True)

    product = relationship("Product", back_populates="variants")





class ProductFeature(Base):
    __tablename__ = "product_features"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    feature_text = Column(String, nullable=False)
    feature_order = Column(Integer, nullable=True)

    product = relationship("Product", back_populates="features")
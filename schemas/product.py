from pydantic import BaseModel
from typing import List, Optional


class FeatureCreate(BaseModel):
    feature_text: str
    feature_order:int


class FeatureResponse(BaseModel):
    id: int
    feature_text: str

    class Config:
        from_attributes = True


class VariantCreate(BaseModel):
    size: str 
    pads_count: int 
    stock: int
    variant_order:int


class VariantResponse(BaseModel):
    id: int
    size: str
    pads_count: int
    stock: int

    class Config:
        from_attributes = True


# ---------------------- PRODUCT SCHEMAS ----------------------
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    image_url: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int
    rating: float
    review_count: int
    is_active: bool
    variants: List[VariantResponse] = []
    features: List[FeatureResponse] = []

    class Config:
        from_attributes = True


class VariantUpdate(BaseModel):
    size: Optional[str] = None
    pads_count: Optional[int] = None
    stock: Optional[int] = None


class FeatureUpdate(BaseModel):
    feature_text: Optional[str] = None

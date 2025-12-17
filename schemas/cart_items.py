from pydantic import BaseModel
from typing import Optional


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int
    variant_order: Optional[int] = None


class CartItemUpdate(BaseModel):
    quantity: int
    variant_order: Optional[int] = None


class CartItemOut(BaseModel):
    id: int
    product_id: int
    variant_order: Optional[int] = None
    quantity: int
    price: float
    model_config = {"from_attributes": True}
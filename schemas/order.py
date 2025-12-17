from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderItemOut(BaseModel):
    id: int  # order_item_id
    order_id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderOut(BaseModel):
    id: int  # order_id
    user_id: int
    total_amount: float
    status: str  # pending, shipped, delivered
    order_date: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True

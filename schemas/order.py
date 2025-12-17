from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderItemOut(BaseModel):
    id: int  
    order_id: int
    product_id: int
    quantity: int
    price: float
    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderOut(BaseModel):
    id: int 
    user_id: int
    total_amount: float
    status: str  
    order_date: datetime
    items: List[OrderItemOut] = []
    model_config = {"from_attributes": True}

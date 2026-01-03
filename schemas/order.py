from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class OrderOut(BaseModel):
    id: int 
    user_id: int
    product_id: int
    quantity: int
    total_amount: float
    status: str  
    order_date: datetime
    model_config = {"from_attributes": True}

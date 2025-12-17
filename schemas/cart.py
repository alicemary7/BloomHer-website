from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from schemas.cart_items import CartItemOut

class CartCreate(BaseModel):
    user_id: int

class CartOut(BaseModel):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    items: List[CartItemOut] = []
    model_config = {"from_attributes": True}

class CartSummary(BaseModel):
    id: int
    user_id: int
    total_items: int
    total_price: float
    is_active: bool
    created_at: datetime
        

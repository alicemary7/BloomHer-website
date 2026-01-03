from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CartCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    is_active: bool
    created_at: datetime
    model_config = {"from_attributes": True}
        

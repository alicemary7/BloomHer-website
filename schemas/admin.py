from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AdminCreate(BaseModel):
    user_id: Optional[int] = None
    email: str
    password: str
    is_super: bool = False


class AdminOut(BaseModel):
    id: int
    user_id: Optional[int]
    email: str
    is_super: bool
    created_at: datetime

    class Config:
        from_attributes = True

from datetime import datetime
from pydantic import BaseModel

class SignupSchema(BaseModel):
    username: str
    email: str
    password: str
    phone: str
    created_at: datetime
    updated_at: datetime

class LoginSchema(BaseModel):
    username:str
    password:str




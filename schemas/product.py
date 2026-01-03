from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    size: str
    pad_count: int
    features: str
    stock: int
    image_url: str



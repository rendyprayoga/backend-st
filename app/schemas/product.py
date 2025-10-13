from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    stock: int
    status: str
    image_url: Optional[str]= None

    @field_validator('price', mode='before')
    def convert_price(cls, value):
        if isinstance(value, str):
            return float(value.replace('.', ''))
        return value

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock: Optional[int] = None
    status: Optional[str] = None
    image_url: Optional[str]= None

class ProductResponse(BaseModel):
    id: str  
    name: str
    description: str
    price: float
    category: str
    stock: int
    status: str
    image_url: Optional[str]= None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
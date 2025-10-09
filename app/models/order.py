from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from .user import PyObjectId

class OrderItem(BaseModel):
    product_id: PyObjectId
    quantity: int
    price: float

class Order(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"  # pending, completed, cancelled
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "items": [
                    {
                        "product_id": "607f1f77bcf86cd799439012",
                        "quantity": 2,
                        "price": 199.98
                    }
                ],
                "total_amount": 199.98,
                "status": "pending"
            }
        }
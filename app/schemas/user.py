from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role:Optional[str] = "user"
    phone: Optional[str] = None
    profile_picture: Optional[str]=None 

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword",
                "full_name": "John Doe",
                "role": "admin",
                 "phone": "+62823456789",
                "profile_picture": "/uploads/profile.jpg"
            }
        }


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None  
    is_active: Optional[bool] = None
    phone:Optional[str] = None
    profile_picture: Optional[str]=None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: Optional[str] = None   
    is_active: bool
    phone: Optional[str] = None
    profile_picture: Optional[str]=None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
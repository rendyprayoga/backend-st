from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActivityLogBase(BaseModel):
    action: str
    resource: str
    resource_id: Optional[str] = None
    user_id: Optional[str] = None
    details: Optional[dict] = None

class ActivityLogCreate(ActivityLogBase):
    pass

class ActivityLogResponse(ActivityLogBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class TopActivityResponse(BaseModel):
    action: str
    count: int

    class Config:
        from_attributes = True
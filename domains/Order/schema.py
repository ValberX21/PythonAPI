from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderBase(BaseModel):
    model_id: int
    sizes: str  # e.g., "40,41,42"
    quantity: int
    customization: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

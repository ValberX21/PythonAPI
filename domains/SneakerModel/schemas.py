from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class SneakerBase(BaseModel):
    model_name: str = Field(..., example="Air Max 90")
    sku: str = Field(..., example="AM90-BLK")
    sizes_available: List[int] = Field(..., example=[38, 39, 40, 41, 42])
    colors: List[str] = Field(..., example=["Black", "White", "Red"])
    material: str = Field(..., example="Mesh and Leather")
    price: float = Field(..., example=199.99)
    is_active: bool = True


class SneakerCreate(SneakerBase):
    pass


class SneakerUpdate(BaseModel):
    model_name: Optional[str]
    sku: Optional[str]
    sizes_available: Optional[List[int]]
    colors: Optional[List[str]]
    material: Optional[str]
    price: Optional[float]
    is_active: Optional[bool]


class Sneaker(SneakerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

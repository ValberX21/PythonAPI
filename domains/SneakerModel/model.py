from sqlalchemy import Column, String, Float, Boolean, DateTime
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func
from database.connection import Base
import uuid

class SneakerModel(Base):
    __tablename__ = "sneakers"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4, index=True)
    model_name = Column(String(150), nullable=False)
    sku = Column(String(100), unique=True, index=True, nullable=False)  # ✅ fixed here
    sizes_available = Column(String, nullable=False)  # JSON string
    colors = Column(String, nullable=False)           # JSON string
    material = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func
from database.connection import Base
from database.connection import Base, engine
Base.metadata.create_all(bind=engine)

class SneakerModel(Base):
    __tablename__ = "sneakers"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(150), nullable=False)
    sku = Column(String(100), unique=True, index=True, nullable=False) 
    sizes_available = Column(String, nullable=False)  
    colors = Column(String, nullable=False)           
    material = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

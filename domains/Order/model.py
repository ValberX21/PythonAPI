from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.connection import Base, engine
from sqlalchemy.orm import relationship

Base.metadata.create_all(bind=engine)

class Order(Base):
    __tablename__ = "sneaker_orders"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("sneakers.id"), nullable=False)
    model = relationship("SneakerModel", backref="orders")
    sizes = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    customization = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

from http.client import HTTPException
from domains.Order.schema import OrderCreate
from domains.SneakerModel.model import SneakerModel
from sqlalchemy.orm import Session
from domains.Order.model import Order  
import json

def create_Order(db: Session, order_data: OrderCreate) -> Order:
    sneaker = db.query(SneakerModel).filter(SneakerModel.id == order_data.model_id).first()
    if not sneaker:
        raise HTTPException(status_code=404, detail="Sneaker model not found")

    new_order = Order(
        model_id=order_data.model_id,
        sizes=order_data.sizes,
        quantity=order_data.quantity,
        customization=order_data.customization
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
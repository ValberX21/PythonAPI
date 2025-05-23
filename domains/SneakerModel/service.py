from http.client import HTTPException
from sqlalchemy.orm import Session
from domains.SneakerModel.schemas import SneakerCreate, SneakerUpdate
from domains.SneakerModel.model import SneakerModel  
import json

def create_sneakerModel(db: Session, sneaker: SneakerCreate):
    db_sneaker = SneakerModel(
        model_name=sneaker.model_name,
        sku=sneaker.sku,
        sizes_available=json.dumps(sneaker.sizes_available),
        colors=json.dumps(sneaker.colors),
        material=sneaker.material,
        price=sneaker.price,
        is_active=sneaker.is_active
    )

    db.add(db_sneaker)
    db.commit()
    db.refresh(db_sneaker)
    
    db_sneaker.sizes_available = json.loads(db_sneaker.sizes_available or "[]")
    db_sneaker.colors = json.loads(db_sneaker.colors or "[]")

    return db_sneaker

def get_sneaker(db: Session):
    return db.query(SneakerModel).all()

def update_sneaker(db: Session, sneaker_id: int, update_data: SneakerUpdate):
    db_sneaker = db.query(SneakerModel).filter(SneakerModel.id == sneaker_id).first()

    if not db_sneaker:
        raise HTTPException(status_code=404, detail="Sneaker not found")

    if update_data.model_name is not None:
        db_sneaker.model_name = update_data.model_name
    if update_data.sku is not None:
        db_sneaker.sku = update_data.sku
    if update_data.sizes_available is not None:
        db_sneaker.sizes_available = json.dumps(update_data.sizes_available)
    if update_data.colors is not None:
        db_sneaker.colors = json.dumps(update_data.colors)
    if update_data.material is not None:
        db_sneaker.material = update_data.material
    if update_data.price is not None:
        db_sneaker.price = update_data.price
    if update_data.is_active is not None:
        db_sneaker.is_active = update_data.is_active

    db.commit()
    db.refresh(db_sneaker)

    db_sneaker.sizes_available = json.loads(db_sneaker.sizes_available or "[]")
    db_sneaker.colors = json.loads(db_sneaker.colors or "[]")

    return db_sneaker

def delete_sneaker(db: Session, sneaker_id: int):
    sneaker = db.query(SneakerModel).filter(SneakerModel.id == sneaker_id).first()

    if not sneaker:
        raise HTTPException(status_code=404, detail="Sneaker not found")

    db.delete(sneaker)
    db.commit()
from sqlalchemy.orm import Session
from domains.SneakerModel.schemas import SneakerCreate
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
    
    db_sneaker.sizes_available = json.loads(db_sneaker.sizes_available)
    db_sneaker.colors = json.loads(db_sneaker.colors)

    db.add(db_sneaker)
    db.commit()
    db.refresh(db_sneaker)
    
    return db_sneaker

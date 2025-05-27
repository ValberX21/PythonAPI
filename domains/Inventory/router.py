from fastapi import APIRouter, Depends
from core.security import get_current_user
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from domains.Inventory import service, schemas

router = APIRouter(prefix="/inventory",dependencies=[Depends(get_current_user)], tags=["inventory"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.InventoryCreate)
def create_inventory(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    return service.create_inventory(db, inventory)
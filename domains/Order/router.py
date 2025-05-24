from core.security import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from domains.Order import service, schema

router = APIRouter(prefix="/order",dependencies=[Depends(get_current_user)], tags=["order"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@router.post("/", response_model=schema.OrderCreate)
def create_order(order: schema.OrderCreate, db: Session = Depends(get_db)):
    return service.create_Order(db, order)
  
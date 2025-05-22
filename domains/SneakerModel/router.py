from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from domains.SneakerModel import service, schemas

router = APIRouter(prefix="/sneakermodel", tags=["sneakermodel"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@router.post("/", response_model=schemas.SneakerCreate)
def create_sneaker(sneaker: schemas.SneakerCreate, db: Session = Depends(get_db)):
    return service.create_sneakerModel(db, sneaker)
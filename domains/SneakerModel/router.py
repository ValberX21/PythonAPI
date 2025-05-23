from core.security import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from domains.SneakerModel import service, schemas

router = APIRouter(prefix="/sneakermodel",dependencies=[Depends(get_current_user)], tags=["sneakermodel"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@router.post("/", response_model=schemas.SneakerCreate)
def create_sneaker(sneaker: schemas.SneakerCreate, db: Session = Depends(get_db)):
    return service.create_sneakerModel(db, sneaker)

@router.get("/")
def list_sneakers(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return service.get_sneaker(db)

@router.put("/{sneaker_id}", response_model=schemas.Sneaker)
def update_sneaker(
    sneaker_id: int,
    update_data: schemas.SneakerUpdate,
    db: Session = Depends(get_db),
    current: str = Depends(get_current_user)
):
   return service.update_sneaker(db, sneaker_id, update_data)

@router.delete("/{sneaker_id}")
def deleter_sneaker(
    sneaker_id: int,
    db: Session =  Depends(get_db),
    current: str = Depends(get_current_user) 
):  
    service.delete_sneaker(db, sneaker_id)
    return {"message":"Sneaker deleted successfully"}    
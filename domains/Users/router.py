from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from domains.Users.service import get_users, create_user
from domains.Users.service import UserCreate 
from domains.Users import service, schemas

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    return get_users(db)

@router.post("/", response_model=schemas.UserOut)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db, user)

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return service.login_user(db, user.email, user.password)

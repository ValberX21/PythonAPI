from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from domains.Users import service, schemas
from core.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@router.get("/")
def list_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return service.get_users(db)

@router.post("/", response_model=schemas.UserOut)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db, user)

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return service.login_user(db, user.email, user.password)

from core.security import create_access_token
from sqlalchemy.orm import Session
from domains.Users.model import User as UserModel
from domains.Users.schemas import UserCreate
from passlib.hash import bcrypt
import domains.Users.schemas as schemas

def get_users(db: Session):
    return db.query(UserModel).all()

def create_user(db: Session, user: UserCreate):
    hashed = bcrypt.hash(user.password)
    db_user = UserModel(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, email: str, password: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if not bcrypt.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
     }
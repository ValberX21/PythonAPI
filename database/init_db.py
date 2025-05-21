from database.connection import Base, engine
from domains.Users.schemas import UserCreate

def init_db():
    Base.metadata.create_all(bind=engine)

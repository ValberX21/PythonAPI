from fastapi import FastAPI
from domains.Users import user_router
from domains.SneakerModel import sneakerModel_router
from database.init_db import init_db
from fastapi.middleware.cors import CORSMiddleware
from database.connection import Base, engine
app = FastAPI()

Base.metadata.create_all(bind=engine)


origins = [ 
        "http://localhost:4200"
]

app.add_middleware(
       CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,
    allow_methods=["*"],            
    allow_headers=["*"],
)

init_db()

app.include_router(user_router)
app.include_router(sneakerModel_router)

@app.get("/")
def read_root():
    return {"message":"Api running"}
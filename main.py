from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import models
from models import Todos
from database import enigne, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=enigne)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependecy = Annotated[Session, Depends(get_db)]
        
@app.get("/")
async def read_all(db: db_dependecy):
    return db.query(Todos).all()
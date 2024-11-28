from fastapi import FastAPI
import models
from database import enigne
from routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=enigne)

app.include_router(auth.router)
app.include_router(todos.router)
from fastapi import FastAPI
import models
from database import enigne

app = FastAPI()

models.Base.metadata.create_all(bind=enigne)
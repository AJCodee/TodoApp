from fastapi import FastAPI, Request
import models
from database import engine
from routers import auth, todos, admin, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/healthy")
async def health_check():
    return {"status": "Server is healthy"}

# Adding all the different routers to activate them.
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

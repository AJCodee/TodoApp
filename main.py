from fastapi import FastAPI, Request, status
import models
from database import engine
from routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

# function to clarify server is healthy.
@app.get("/healthy")
async def health_check():
    return {"status": "Server is healthy"}

# Adding all the different routers to activate them.
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

from fastapi import FastAPI

from routes.user import router as user
from routes.token import router as token
from routes.todo import router as todo
from routes.project import router as project

app = FastAPI()

app.include_router(user, prefix="/user", tags=["user"])

app.include_router(token, prefix="/token", tags=["token"])

app.include_router(todo, prefix="/todo", tags=["todo"])

app.include_router(project, prefix="/project", tags=["project"])

from fastapi import FastAPI

from routes.user import router as user
from routes.token import router as token

app = FastAPI()

app.include_router(user, prefix="/user", tags=["user"])

app.include_router(token, prefix="/token", tags=["token"])

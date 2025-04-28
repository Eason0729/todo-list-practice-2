from pydantic import BaseModel
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from models import Users, get_db

from auth import AuthController, get_auth_ctrl, UserId

router = APIRouter(tags=["token"])


class LoginRequest(BaseModel):
    username: str | None
    password: str
    email: str | None


class LoginResponse(BaseModel):
    token: str
    user_id: int


@router.post("/", response_model=LoginResponse)
def create_token(
    request: LoginRequest,
    db: Session = Depends(get_db),
    auth: AuthController = Depends(get_auth_ctrl),
):
    if LoginRequest.username is None and LoginRequest.email is None:
        raise HTTPException(status_code=400, detail="Username or email is required")

    if LoginRequest.username is not None:
        user = db.query(Users).filter(Users.username == request.username).first()
    else:
        user = db.query(Users).filter(Users.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not auth.verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = auth.create_access_token(UserId(user.id))

    return {"token": token, "user_id": user.id}


class VerifyTokenRequest(BaseModel):
    token: str


class VerifyTokenResponse(BaseModel):
    verified: bool


@router.patch("/", response_model=VerifyTokenResponse)
def verify_token(
    request: VerifyTokenRequest, auth: AuthController = Depends(get_auth_ctrl)
):
    try:
        auth.verify_and_decode_access_token(request.token)
    except Exception:
        return {"verified": False}

    return {"verified": True}

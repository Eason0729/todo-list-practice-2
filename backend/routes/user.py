from pydantic import BaseModel
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from models import Users, get_db, Paginate

from argon2 import PasswordHasher

hasher = PasswordHasher()

router = APIRouter(tags=["user"])


class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str


class CreateUserResponse(BaseModel):
    id: int


@router.post("/", response_model=CreateUserResponse)
def create_user(request: CreateUserRequest, db: Session = Depends(get_db)):
    hashed_password = hasher.hash(request.password)
    user = Users(
        username=request.username, password_hash=hashed_password, email=request.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user": {"id": user.id}}


class GetUserResponse(BaseModel):
    id: int
    username: str
    email: str


@router.get("/{user_id}", response_model=GetUserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    }


class PartialUser(BaseModel):
    id: int
    username: str


class ListUsersResponse(BaseModel):
    users: list[PartialUser]
    next_session: str


@router.get("s/create/{page_size}", response_model=ListUsersResponse)
def create_user_pagination(page_size: int, db: Session = Depends(get_db)):
    paginate = Paginate(page_size)
    users = paginate.apply(db.query(Users.id, Users.username)).all()
    paginate.next_page()

    users = [{"id": user[0], "username": user[1]} for user in users]

    return {"users": users, "next_session": paginate.to_token()}


@router.get("s/{pagination}", response_model=ListUsersResponse)
def get_users_by_pagination(pagination: str, db: Session = Depends(get_db)):
    paginate = Paginate.from_token(pagination)
    users = paginate.apply(db.query(Users.id, Users.username)).all()
    paginate.next_page()

    users = [{"id": user[0], "username": user[1]} for user in users]

    return {"users": users, "next_session": paginate.next_page()}

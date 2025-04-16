import datetime
from os import getenv
import secrets
from argon2 import PasswordHasher

from typing import Generator
import jwt

from pydantic import BaseModel

SECRET_KEY = (
    getenv("JWT_SECRET")
    if getenv("JWT_SECRET") is not None
    else secrets.token_urlsafe(32)
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class UserId(BaseModel):
    user_id: int

    def __init__(self, user_id: int):
        super().__init__(user_id=user_id)
        self.user_id = user_id


class TokenGenerator:
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    def __init__(
        self, secret_key: str, algorithm: str, access_token_expire_minutes: int
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(self, user: UserId):
        to_encode = {"id": user.user_id}
        expire = datetime.utcnow() + datetime.timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    def verify_and_decode_access_token(self, token: str) -> UserId:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: int = payload.get("id")
            if user_id is None:
                raise ValueError("Invalid token")
            return UserId(user_id=user_id)
        except Exception as e:
            raise ValueError(f"An error occurred while decoding the token: {str(e)}")


class AuthController:
    hasher: PasswordHasher
    tokenGen: TokenGenerator

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expire_minutes: int,
    ):
        self.tokenGen = TokenGenerator(
            secret_key=secret_key,
            algorithm=algorithm,
            access_token_expire_minutes=access_token_expire_minutes,
        )
        self.hasher = PasswordHasher()

    def create_access_token(self, user: UserId):
        return self.tokenGen.create_access_token(user)

    def verify_and_decode_access_token(self, token: str) -> UserId:
        return self.tokenGen.verify_and_decode_access_token(token)

    def hash_password(self, password: str) -> str:
        return self.hasher.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        try:
            return self.hasher.verify(hashed_password, password)
        except Exception as e:
            raise ValueError(
                f"An error occurred while verifying the password: {str(e)}"
            )


def get_auth_ctrl() -> Generator[AuthController, None, None]:
    auth_ctrl = AuthController(
        secret_key=SECRET_KEY,
        algorithm=ALGORITHM,
        access_token_expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    yield auth_ctrl

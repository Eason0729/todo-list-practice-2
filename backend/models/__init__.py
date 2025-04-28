# ruff: noqa: F401
from typing import Generator
from .project_members import ProjectMembers
from .projects import Projects
from .todos import Todos
from .users import Users
from .paginate import Paginate

from os import getenv

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

DATABASE_URL = str(
    getenv("DATABASE_URL")
    if getenv("DATABASE_URL") is not None
    else "postgresql://postgres_user:PassWWdd@localhost:5432/prac_db"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

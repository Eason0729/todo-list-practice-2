# ruff: noqa: F821
from typing import List, Optional

from sqlalchemy import (
    DateTime,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from .base import Base


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="users_pkey"),
        UniqueConstraint("email", name="users_email_key"),
        UniqueConstraint("username", name="users_username_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("now()")
    )

    projects: Mapped[List["Projects"]] = relationship(
        "Projects", back_populates="owner"
    )
    project_members: Mapped[List["ProjectMembers"]] = relationship(
        "ProjectMembers", back_populates="user"
    )
    todos: Mapped[List["Todos"]] = relationship("Todos", back_populates="user")

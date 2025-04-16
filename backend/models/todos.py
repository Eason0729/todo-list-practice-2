# ruff: noqa: F821
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

from .base import Base


class Todos(Base):
    __tablename__ = "todos"
    __table_args__ = (
        ForeignKeyConstraint(
            ["project_id"], ["projects.id"], name="todos_project_id_fkey"
        ),
        ForeignKeyConstraint(["user_id"], ["users.id"], name="todos_user_id_fkey"),
        PrimaryKeyConstraint("id", name="todos_pkey"),
        Index("idx_todos_due_date", "due_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    priority: Mapped[int] = mapped_column(Integer)
    project_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    content: Mapped[Optional[str]] = mapped_column(Text)
    due_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    is_completed: Mapped[Optional[bool]] = mapped_column(Boolean)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("now()")
    )

    project: Mapped["Projects"] = relationship("Projects", back_populates="todos")
    user: Mapped["Users"] = relationship("Users", back_populates="todos")

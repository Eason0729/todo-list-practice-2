# ruff: noqa: F821
from typing import List, Optional

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

from .base import Base


class Projects(Base):
    __tablename__ = "projects"
    __table_args__ = (
        ForeignKeyConstraint(["owner_id"], ["users.id"], name="projects_owner_id_fkey"),
        PrimaryKeyConstraint("id", name="projects_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    owner_id: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("now()")
    )

    owner: Mapped["Users"] = relationship("Users", back_populates="projects")
    project_members: Mapped[List["ProjectMembers"]] = relationship(
        "ProjectMembers", back_populates="project"
    )
    todos: Mapped[List["Todos"]] = relationship("Todos", back_populates="project")

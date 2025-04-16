# ruff: noqa: F821
from typing import Optional

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

from .base import Base


class ProjectMembers(Base):
    __tablename__ = "project_members"
    __table_args__ = (
        ForeignKeyConstraint(
            ["project_id"], ["projects.id"], name="project_members_project_id_fkey"
        ),
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="project_members_user_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="project_members_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    role: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("now()")
    )

    project: Mapped["Projects"] = relationship(
        "Projects", back_populates="project_members"
    )
    user: Mapped["Users"] = relationship("Users", back_populates="project_members")

"""create todos

Revision ID: a719da8b79b3
Revises: 5c41579a7c4a
Create Date: 2025-04-14 15:42:23.711696

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "a719da8b79b3"
down_revision: Union[str, None] = "5c41579a7c4a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "todos",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column("is_completed", sa.Boolean(), default=False),
        sa.Column(
            "project_id", sa.Integer(), sa.ForeignKey("projects.id"), nullable=False
        ),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_todos_due_date", "todos", ["due_date"])


def downgrade() -> None:
    op.drop_index("idx_todos_due_date", table_name="todos")
    op.drop_table("todos")

"""create project

Revision ID: 5c41579a7c4a
Revises: d18247e2bef6
Create Date: 2025-04-14 15:41:56.791466

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "5c41579a7c4a"
down_revision: Union[str, None] = "d18247e2bef6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("projects")

"""create project members(pivot tabel)

Revision ID: e0e3385080e5
Revises: a719da8b79b3
Create Date: 2025-04-14 15:43:25.527199

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "e0e3385080e5"
down_revision: Union[str, None] = "a719da8b79b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "project_members",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "project_id", sa.Integer(), sa.ForeignKey("projects.id"), nullable=False
        ),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "role", sa.String(length=50), nullable=False
        ),  # e.g., 'owner', 'editor', 'viewer'
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("project_members")

"""Initial schema

Revision ID: 9a422a342277
Revises: 
Create Date: 2026-07-16 00:57:36.270900

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a422a342277'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column("num_ideas", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "ideas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("startup_idea", sa.String(), nullable=False),
        sa.Column("creativity_sentence", sa.String(), nullable=True),
        sa.Column("creativity_score", sa.Integer(), nullable=True),
        sa.Column("demand_sentence", sa.String(), nullable=True),
        sa.Column("demand_score", sa.Integer(), nullable=True),
        sa.Column("uniqueness_sentence", sa.String(), nullable=True),
        sa.Column("uniqueness_score", sa.Integer(), nullable=True),
        sa.Column("scale_sentence", sa.String(), nullable=True),
        sa.Column("scale_score", sa.Integer(), nullable=True),
        sa.Column("investment_sentence", sa.String(), nullable=True),
        sa.Column("investment_score", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ideas_id"), "ideas", ["id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_ideas_id"), table_name="ideas")
    op.drop_table("ideas")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")

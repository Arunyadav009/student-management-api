
"""create initial students table

Revision ID: 1c2d3e4f5a6b
Revises:
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1c2d3e4f5a6b"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "students",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("course", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_students_id"),
        "students",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_students_id"), table_name="students")
    op.drop_table("students")

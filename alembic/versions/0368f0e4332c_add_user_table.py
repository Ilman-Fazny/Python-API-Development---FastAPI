"""add user table

Revision ID: 0368f0e4332c
Revises: 38c934fdb6b1
Create Date: 2026-06-08 00:57:49.429356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0368f0e4332c'
down_revision: Union[str, Sequence[str], None] = '38c934fdb6b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
            )


def downgrade() -> None:
    op.drop_table('users')

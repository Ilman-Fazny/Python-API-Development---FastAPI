"""add content column to posts table

Revision ID: 38c934fdb6b1
Revises: 5da95f3db478
Create Date: 2026-06-08 00:48:52.948507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38c934fdb6b1'
down_revision: Union[str, Sequence[str], None] = '5da95f3db478'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

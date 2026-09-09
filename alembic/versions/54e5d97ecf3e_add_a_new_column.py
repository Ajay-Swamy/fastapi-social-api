"""add a new column

Revision ID: 54e5d97ecf3e
Revises: baf9f29a2dfb
Create Date: 2026-09-08 15:21:04.530598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54e5d97ecf3e'
down_revision: Union[str, Sequence[str], None] = 'baf9f29a2dfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String,nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass

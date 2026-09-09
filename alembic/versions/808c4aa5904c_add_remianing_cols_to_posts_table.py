"""add remianing cols to posts table

Revision ID: 808c4aa5904c
Revises: 13c9963476d7
Create Date: 2026-09-08 16:25:29.890125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '808c4aa5904c'
down_revision: Union[str, Sequence[str], None] = '13c9963476d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass

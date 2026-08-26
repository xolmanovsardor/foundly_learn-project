"""add_users_missing_columns

Revision ID: 40b82f1a8944
Revises: 20581ae0310f
Create Date: 2026-08-26 21:29:33.964759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40b82f1a8944'
down_revision: Union[str, Sequence[str], None] = '20581ae0310f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

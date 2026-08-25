"""add first_name to users

Revision ID: 20581ae0310f
Revises: c47e71fae8cd
Create Date: 2026-08-25 15:39:27.964233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20581ae0310f'
down_revision: Union[str, Sequence[str], None] = 'c47e71fae8cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

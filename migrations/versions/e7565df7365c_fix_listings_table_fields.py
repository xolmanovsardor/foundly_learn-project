"""fix listings table fields

Revision ID: e7565df7365c
Revises: 971d4eb909de
Create Date: 2026-08-25 15:19:43.058809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7565df7365c'
down_revision: Union[str, Sequence[str], None] = '971d4eb909de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

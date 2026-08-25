"""Add listings table

Revision ID: 971d4eb909de
Revises: 01d9d2b96494
Create Date: 2026-08-25 14:55:38.241631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '971d4eb909de'
down_revision: Union[str, Sequence[str], None] = '01d9d2b96494'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""add_date_found_to_listings

Revision ID: a33e2ecd8398
Revises: 40b82f1a8944
Create Date: 2026-08-26 22:02:26.690881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a33e2ecd8398'
down_revision: Union[str, Sequence[str], None] = '40b82f1a8944'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

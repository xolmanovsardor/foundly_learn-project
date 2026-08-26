"""add_dekete_serche_current_user_ect

Revision ID: 27335492712f
Revises: a33e2ecd8398
Create Date: 2026-08-26 22:38:29.180070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27335492712f'
down_revision: Union[str, Sequence[str], None] = 'a33e2ecd8398'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

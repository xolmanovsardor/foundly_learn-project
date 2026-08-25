"""update listings fields

Revision ID: c47e71fae8cd
Revises: e7565df7365c
Create Date: 2026-08-25 15:29:38.202304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c47e71fae8cd'
down_revision: Union[str, Sequence[str], None] = 'e7565df7365c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

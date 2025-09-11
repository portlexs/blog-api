"""delete alembic_ini

Revision ID: bea775576a5a
Revises: e6706f96354a
Create Date: 2025-09-10 20:45:19.186861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bea775576a5a'
down_revision: Union[str, Sequence[str], None] = 'e6706f96354a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

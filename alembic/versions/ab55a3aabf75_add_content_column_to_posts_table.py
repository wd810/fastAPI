"""add content column to posts table

Revision ID: ab55a3aabf75
Revises: 82cce6e8ab1f
Create Date: 2022-07-19 22:29:30.277766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab55a3aabf75'
down_revision = '82cce6e8ab1f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

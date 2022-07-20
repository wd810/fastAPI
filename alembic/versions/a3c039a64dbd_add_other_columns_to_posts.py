"""add other columns to posts

Revision ID: a3c039a64dbd
Revises: 90cc4af67802
Create Date: 2022-07-19 23:31:59.925280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3c039a64dbd'
down_revision = '90cc4af67802'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass

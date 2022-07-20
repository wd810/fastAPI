"""create posts table

Revision ID: 82cce6e8ab1f
Revises: 
Create Date: 2022-07-18 23:05:26.200141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82cce6e8ab1f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass

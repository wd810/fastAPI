"""add foreigh-key to posts table

Revision ID: 90cc4af67802
Revises: 1e26bde0709e
Create Date: 2022-07-19 23:25:37.075378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90cc4af67802'
down_revision = '1e26bde0709e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass

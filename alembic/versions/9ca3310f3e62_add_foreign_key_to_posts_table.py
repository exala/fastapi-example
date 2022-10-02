"""add foreign key to posts table

Revision ID: 9ca3310f3e62
Revises: ab64680942a2
Create Date: 2022-10-02 08:39:13.281843

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ca3310f3e62'
down_revision = 'ab64680942a2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('post_user_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass

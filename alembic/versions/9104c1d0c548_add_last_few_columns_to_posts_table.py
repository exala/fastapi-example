"""add last few columns to posts table

Revision ID: 9104c1d0c548
Revises: 9ca3310f3e62
Create Date: 2022-10-02 08:48:27.779982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9104c1d0c548'
down_revision = '9ca3310f3e62'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='True'))
    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass

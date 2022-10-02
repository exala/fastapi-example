"""add content column to post table

Revision ID: da854377b4ca
Revises: a39d9b18b2b8
Create Date: 2022-10-02 08:24:03.154528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da854377b4ca'
down_revision = 'a39d9b18b2b8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

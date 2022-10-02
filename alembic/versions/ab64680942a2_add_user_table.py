"""add user table

Revision ID: ab64680942a2
Revises: da854377b4ca
Create Date: 2022-10-02 08:27:56.187178

"""
from alembic import op
import sqlalchemy as sa
from pydantic import EmailStr


# revision identifiers, used by Alembic.
revision = 'ab64680942a2'
down_revision = 'da854377b4ca'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
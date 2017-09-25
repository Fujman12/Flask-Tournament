"""empty message

Revision ID: 0d8469473d50
Revises: 8590e9460f6c
Create Date: 2017-09-25 11:33:08.157290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d8469473d50'
down_revision = '8590e9460f6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member', sa.Column('role', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('member', 'role')
    # ### end Alembic commands ###
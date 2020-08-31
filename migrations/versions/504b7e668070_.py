"""empty message

Revision ID: 504b7e668070
Revises: c57dcf2a2bc2
Create Date: 2020-08-31 12:58:44.695359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '504b7e668070'
down_revision = 'c57dcf2a2bc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('actors', 'test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actors', sa.Column('test', sa.VARCHAR(length=6), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

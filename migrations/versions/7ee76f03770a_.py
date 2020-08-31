"""empty message

Revision ID: 7ee76f03770a
Revises: f495af5797d5
Create Date: 2020-08-31 16:46:36.814652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ee76f03770a'
down_revision = 'f495af5797d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('release_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movies', 'release_date')
    # ### end Alembic commands ###

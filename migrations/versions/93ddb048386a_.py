"""empty message

Revision ID: 93ddb048386a
Revises: be2edab8d150
Create Date: 2020-08-21 01:16:47.843178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93ddb048386a'
down_revision = 'be2edab8d150'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movies', 'movie_details_test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('movie_details_test', sa.VARCHAR(length=200), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

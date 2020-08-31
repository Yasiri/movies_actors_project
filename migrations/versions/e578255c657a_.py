"""empty message

Revision ID: e578255c657a
Revises: 16c6c203cfac
Create Date: 2020-08-27 08:46:54.286567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e578255c657a'
down_revision = '16c6c203cfac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('M_A_association')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('M_A_association',
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('actor_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], name='M_A_association_actor_id_fkey'),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], name='M_A_association_movie_id_fkey'),
    sa.PrimaryKeyConstraint('movie_id', 'actor_id', name='M_A_association_pkey')
    )
    # ### end Alembic commands ###

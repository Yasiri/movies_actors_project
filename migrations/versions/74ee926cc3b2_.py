"""empty message

Revision ID: 74ee926cc3b2
Revises: a8d709acc153
Create Date: 2020-08-27 10:38:26.373004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74ee926cc3b2'
down_revision = 'a8d709acc153'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies_actors', sa.Column('actor_id', sa.Integer(), nullable=True))
    op.add_column('movies_actors', sa.Column('movie_id', sa.Integer(), nullable=True))
    op.drop_constraint('movies_actors_movie_id_F_fkey', 'movies_actors', type_='foreignkey')
    op.drop_constraint('movies_actors_actor_id_F_fkey', 'movies_actors', type_='foreignkey')
    op.create_foreign_key(None, 'movies_actors', 'movies', ['movie_id'], ['id'], ondelete='cascade')
    op.create_foreign_key(None, 'movies_actors', 'actors', ['actor_id'], ['id'], ondelete='cascade')
    op.drop_column('movies_actors', 'actor_id_F')
    op.drop_column('movies_actors', 'movie_id_F')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies_actors', sa.Column('movie_id_F', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('movies_actors', sa.Column('actor_id_F', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'movies_actors', type_='foreignkey')
    op.drop_constraint(None, 'movies_actors', type_='foreignkey')
    op.create_foreign_key('movies_actors_actor_id_F_fkey', 'movies_actors', 'actors', ['actor_id_F'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('movies_actors_movie_id_F_fkey', 'movies_actors', 'movies', ['movie_id_F'], ['id'], ondelete='CASCADE')
    op.drop_column('movies_actors', 'movie_id')
    op.drop_column('movies_actors', 'actor_id')
    # ### end Alembic commands ###

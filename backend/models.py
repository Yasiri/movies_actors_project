import os
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import json
import psycopg2
import datetime

# # for heroku deployment
database_path = os.environ['DATABASE_URL']
conn = psycopg2.connect(database_path, sslmode='require')

# print('path ', database_path)
# database_name = "capstoon"
# # database_name = "capstone_test"
# database_path = "postgresql://{}:{}@{}/{}".format(
#     'yaser', 'yaser', 'localhost:5432', database_name)


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = 'GDtfDCFYjD'
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Movies
'''


# ----------------------------------------------------------------------------#
# Models. Movies & Actors
# ----------------------------------------------------------------------------#


class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    movie_details = db.Column(db.String(200))
    actors = db.relationship("Actors", secondary="movies_actors")

    '''
    short()
        short form representation of the Movie model
    '''

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'movie_details': self.movie_details
        }

    '''
    long()
        long form representation of the Movie model
    '''

    def long(self):
        # movieDate = datetime.datetime(self.release_date.year, 1, 1)
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,  # movieDate.strftime("%Y")
            'movie_details': self.movie_details
        }

    def __repr__(self):
        return json.dumps(self.short())
        # return f"<movie {self.id} {self.title}>"

    def __init__(self, title, release_date, movie_details):
        self.title = title
        self.release_date = release_date
        self.movie_details = movie_details

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'movie_details': self.movie_details
        }


class Actors(db.Model):
    __tablename__ = "actors"

    id = db.Column(db.Integer, primary_key=True)
    actorName = db.Column(db.String(80), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    movies = db.relationship("Movies", secondary="movies_actors")
    '''
    short()
        short form representation of the Movie model
    '''

    def short(self):
        return {
            'id': self.id,
            'actorName': self.actorName,
            'age': self.age,
            'gender': self.gender
        }

    '''
    long()
        long form representation of the Movie model
    '''

    def long(self):
        return {
            'id': self.id,
            'actorName': self.actorName,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return f"<Actor {self.id} {self.actorName} {self.age} {self.gender}>"

    def __init__(self, actorName, age, gender):
        self.actorName = actorName
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        """returns a formatted response of the data in the model"""
        return {
            'id': self.id,
            'actorName': self.actorName,
            'age': self.age,
            'gender': self.gender
        }


class M_A_association(db.Model):
    __tablename__ = 'movies_actors'
    id = db.Column(db.Integer, primary_key=True)
    movie_id_a = db.Column(db.Integer,  db.ForeignKey(
        'movies.id', ondelete="cascade"))
    actor_id_a = db.Column(db.Integer,  db.ForeignKey(
        'actors.id', ondelete="cascade"))
    movie = db.relationship(Movies, backref=db.backref(
        "movies_actors", cascade="all, delete-orphan"))
    actor = relationship(Actors, backref=db.backref(
        "movies_actors", cascade="all, delete-orphan"))

    def short(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id_a,
            'actor_id': self.actor_id_a
        }

    def __repr__(self):
        return json.dumps(self.short())
        # return f"<movie {self.id} {self.title}>"

    def __init__(self, movie_id, actor_id):
        self.movie_id_a = movie_id
        self.actor_id_a = actor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id_a,
            'actor_id': self.actor_id_a
        }

import os
import json

from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

from utils import ReleaseDate

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


movie_actor_association = db.Table('movie_actor_association',
                                Column('movie_id', Integer,
                                       ForeignKey('movies.id'),
                                       primary_key=True),
                                Column('actor_id', Integer,
                                       ForeignKey('actors.id'),
                                       primary_key=True),
                                )


class Movies(db.Model):
    '''
    Movies
    '''
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    actors = relationship('Actors',
                          secondary=movie_actor_association,
                          back_populates='movies',
                          lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': ReleaseDate.date_object_to_string(self.release_date),
        }


class Actors(db.Model):
    '''
    Actors
    '''
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(Boolean)
    movies = relationship('Movies',
                          secondary=movie_actor_association,
                          back_populates='actors',
                          lazy=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }
import os
import json

from sqlalchemy import Column, String, Integer, Boolean, Date, \
    Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


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


'''
Person
Have title and release year
'''


# class Person(db.Model):
#     __tablename__ = 'People'

#     id = Column(db.Integer, primary_key=True)
#     name = Column(String)
#     catchphrase = Column(String)

#     def __init__(self, name, catchphrase=""):
#         self.name = name
#         self.catchphrase = catchphrase

#     def format(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'catchphrase': self.catchphrase}


movie_actor_table = Table('movie_actor_items', MetaData(),
                          Column('movie_id', Integer,
                                 ForeignKey('Movies.id'),
                                 primary_key=True),
                          Column('actor_id', Integer,
                                 ForeignKey('Actors.id'),
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
                          secondary=movie_actor_table,
                          back_populates='movies',
                          lazy=True)


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
                          secondary=movie_actor_table,
                          back_populates='movies',
                          lazy=True)

import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.drop_all()
    db.create_all()


'''
class Person(db.Model):  
  __tablename__ = 'People'

  id = Column(db.Integer, primary_key=True)
  name = Column(String)
  catchphrase = Column(String)

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'catchphrase': self.catchphrase}
'''


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    actors_in_movies = db.relationship('ActorsInMovies', backref='actor', lazy=True)

    def short(self):
      return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender
      }
    
    def long(self):
      formatted_movies=[]
      for actor_in_movie in self.actors_in_movies:
        movie = Movie.query.filter_by(id=actor_in_movie.movie_id).first()
        formatted_movies.append(movie.short())
      return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender,
        'movies': formatted_movies
      }
    
    def insert(self):
        try:
          db.session.add(self)
          db.session.commit()
        except:
          db.session.rollback()
          raise
    
    def update(self):
        try:
          db.session.commit()
        except:
          db.session.rollback()
          raise
    
    def delete(self):
        try:
          db.session.delete(self)
          db.session.commit()
        except:
          db.session.rollback()
          raise

    def __repr__(self):
      return'<Actor {}>'.format(self.name)


    # TODO: implement missing fields as a database migration using Flask-Migrate


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    actors_in_movies = db.relationship('ActorsInMovies', backref='movie', lazy=True)

    def short(self):
      return {
          'id': self.id,
          'title': self.title,
          'release_date': self.release_date
      }
    
    def long(self):
      formatted_actors=[]
      for actor_in_movie in self.actors_in_movies:
        actor = Actor.query.filter_by(id=actor_in_movie.actor_id).first()
        formatted_actors.append(actor.short())
      return {
          'id': self.id,
          'title': self.title,
          'release_date': self.release_date,
          'actors': formatted_actors
      }
    
    def insert(self):
        try:
          db.session.add(self)
          db.session.commit()
        except:
          db.session.rollback()
          raise
    
    def update(self):
        try:
          db.session.commit()
        except:
          db.session.rollback()
          raise
    
    def delete(self):
        try:
          db.session.delete(self)
          db.session.commit()
        except:
          db.session.rollback()
          raise
   
    def __repr__(self):
      return'<Movie {}>'.format(self.title)


class ActorsInMovies(db.Model):
    __tablename__ = 'ActorsInMovies'

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('Actor.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint("actor_id", "movie_id"),)
    def long(self):
      return {
          'id': self.id,
          'actor_id': self.actor_id,
          'movie_id': self.movie_id,
      }
    
    def insert(self):
        try:
          db.session.add(self)
          db.session.commit()
        except:
          db.session.rollback()
          raise
    
    def update(self):
        try:
          db.session.commit()
        except:
          db.session.rollback()
          raise
    
    def delete(self):
        try:
          db.session.delete(self)
          db.session.commit()
        except:
          db.session.rollback()
          raise
    
    def __repr__(self):
      return'<Show {}>'.format(self.name)



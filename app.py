import os
import traceback
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Actor, ActorsInMovies, Movie, db
from flask_cors import CORS
from auth import AuthError, requires_auth
import json
from pprint import pprint

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    #ACTORS        

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        actors=Actor.query.order_by(Actor.name).all()
        formatted_actors=[]
        for actor in actors:
            formatted_actors.append(actor.long())
        return jsonify({
            "success":True,
            "actors": formatted_actors
        })


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor():
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        new_actor = Actor(name=name, age=age, gender=gender)
        try:
            new_actor.insert()
            return jsonify({
                "success": True,
                "actor": new_actor.long()
            })
        except Exception as err:
            print(traceback.format_exc())
            abort(422)


    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(actor_id):
        try:
            actor_for_update = Actor.query.filter_by(id=actor_id).all()
            if len(actor_for_update) == 1:
                body=request.get_json()
                name = body.get("name")
                age = body.get("age")
                gender = body.get("gender")
                if name is not None: 
                    actor_for_update[0].name = name
                if age is not None:
                    actor_for_update[0].age = age
                if gender is not None:
                    actor_for_update[0].gender = gender
                actor_for_update[0].update()
                return jsonify({
                    "success":True,
                    "updated":actor_for_update[0].long()
                })
            else:
                abort(404)
        except Exception as err:
            print(traceback.format_exc())
            abort(404)


    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor_id):
        try:
            actor_for_deletion = Actor.query.filter_by(id=actor_id).all()
            if len(actor_for_deletion) == 1:
                actor_for_deletion[0].delete()
                return jsonify({
                    "success":True,
                    "delete": actor_id
                })
            else:
                abort(404)
        except:
            print(traceback.format_exc())
            abort(404)

    #MOVIES

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies():
        movies=Movie.query.order_by(Movie.title).all()
        formatted_movies=[]
        for movie in movies:
            formatted_movies.append(movie.long())
        return jsonify({
            "success":True,
            "movies": formatted_movies
        })


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie():
        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')
        new_movie = Movie(title=title, release_date=release_date)
        try:
            new_movie.insert()
            return jsonify({
                "success": True,
                "movie": new_movie.long()
            })
        except Exception as err:
            print(traceback.format_exc())
            abort(422)


    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(movie_id):
        try:
            movie_for_update = Movie.query.filter_by(id=movie_id).all()
            if len(movie_for_update) == 1:
                body=request.get_json()
                title = body.get("title")
                release_date = body.get("release_date")
                if title is not None: 
                    movie_for_update[0].title = title
                if release_date is not None:
                    movie_for_update[0].release_date = release_date
                movie_for_update[0].update()
                return jsonify({
                    "success":True,
                    "updated":movie_for_update[0].long()
                })
            else:
                abort(404)
        except Exception as err:
            print(traceback.format_exc())
            abort(422)


    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id):
        try:
            movie_for_deletion = Movie.query.filter_by(id=movie_id).all()
            if len(movie_for_deletion) == 1:
                movie_for_deletion[0].delete()
                return jsonify({
                    "success":True,
                    "delete": movie_id
                })
            else:
                abort(404)
        except:
            print(traceback.format_exc())
            abort(404)


    #ACTORS IN MOVIES

    @app.route('/movies/<movie_id>/add_actor', methods=['PATCH'])
    @requires_auth('patch:movies')
    def add_actor_to_movie(movie_id):
        body = request.get_json()
        actor_id = body.get('actor_id')
        new_actor_for_movie = ActorsInMovies(actor_id=actor_id, movie_id=movie_id)
        try:
            new_actor_for_movie.insert()
            return jsonify({
                "success": True,
                "updated_movie": Movie.query.filter_by(id=movie_id).first().long()
            })
        except Exception as err:
            print(traceback.format_exc())
            abort(422)

    @app.route('/movies/<movie_id>/delete_actor', methods=['PATCH'])
    @requires_auth('patch:movies')
    def delete_actor_from_movie(movie_id):
        body = request.get_json()
        actor_id = body.get('actor_id')
        actor_to_delete_from_movie = ActorsInMovies.query.filter_by(movie_id=movie_id, actor_id=actor_id).first()
        try:
            actor_to_delete_from_movie.delete()
            return jsonify({
                "success": True,
                "updated_movie": Movie.query.filter_by(id=movie_id).first().long()
            })
        except Exception as err:
            print(traceback.format_exc())
            abort(422)
    
    
    
    
    #ERROR HANDLERS

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
    
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401
    
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    return app

app = create_app()






if __name__ == '__main__':
    app.run()

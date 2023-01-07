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
        

    @app.route('/actors', methods=['GET'])
    #@requires_auth('get:actors')
    def get_actors():
        actors=Actor.query.order_by(Actor.name).all()
        formatted_actors=[]
        for actor in actors:
            formatted_actors.append(actor.fields_dict())
        return jsonify({
            "success":True,
            "actors": formatted_actors
        })


    @app.route('/actors', methods=['POST'])
    #@requires_auth('post:actors')
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
                "actor": new_actor.fields_dict()
            })
        except Exception as err:
            print(traceback.format_exc())
            abort(422)


    @app.route('/actors/<actor_id>', methods=['PATCH'])
    #@requires_auth('patch:actors')
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
                    "updated":actor_for_update[0].fields_dict()
                })
            else:
                abort(404)
        except Exception as err:
            print(traceback.format_exc())
            abort(422)


    @app.route('/actors/<actor_id>', methods=['DELETE'])
    #@requires_auth('delete:actirs')
    def delete_actor(actor_id):
        try:
            actor_for_deletion = Actor.query.filter_by(id=actor_id).all()
            pprint(actor_for_deletion)
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


    return app

app = create_app()
















'''
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


'''

if __name__ == '__main__':
    app.run()

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, ActorsInMovies


class CapstoneTestCase(unittest.TestCase):
    exec_producer_jwt = os.environ['EXEC_PRODUCER_JWT']
    casting_asst_jwt = os.environ['CASTING_ASST_JWT']
    casting_dir_jwt = os.environ['CASTING_DIR_JWT']
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.drop_all()
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass



    #ACTORS (using executive producer auth)

    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(len(data['actors']), 0)
    
    def test_post_patch_delete_actor(self):
        res = self.client().post('/actors', json={"name": "Tom Cruise", "age": 60, "gender": "M"}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        res = self.client().patch('/actors/1', json={"name": "Tom Hanks", "age": 66}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
        res = self.client().delete('/actors/1', headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_actor_post_fails(self):
        res = self.client().post('/actors', json={"name": "Tom Cruise", "age": "M", "gender": "M"}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
    
    def test_404_if_actor_does_not_exist_on_patch(self):
        res = self.client().patch('/actors/1000', json={"name": "Tom Hanks", "age": 66}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
    
    def test_404_if_actor_does_not_exist_on_delete(self):
        res = self.client().delete('/actors/1000', headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)



    #MOVIES

    def test_get_movies(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(len(data['movies']), 0)
    
    def test_post_patch_delete_movie(self):
        res = self.client().post('/movies', json={"title": "Top Gun", "release_date": "1986-05-16"}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        res = self.client().patch('/movies/1', json={"title": "Rainman", "release_date": "1988-12-12"}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
        res = self.client().delete('/movies/1', headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_movie_post_fails(self):
        res = self.client().post('/movies', json={"title": "Top Gun", "release_date": "InvalidDate"}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
    
    def test_422_if_movie_does_not_exist_on_patch(self):
        res = self.client().patch('/movies/1000', json={"title": "Rainman", "release_date": "1988-12-12"}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
    
    def test_404_if_movie_does_not_exist_on_delete(self):
        res = self.client().delete('/movies/1000', headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)


    #ACTORS IN MOVIES

    def test_associate_actor_with_movie(self):
        #Add an actor
        res = self.client().post('/actors', json={"name": "Tom Cruise", "age": 60, "gender": "M"}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #Add a movie
        res = self.client().post('/movies', json={"title": "Top Gun", "release_date": "1986-05-16"}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #Associate actor with movie
        res = self.client().patch('/movies/1/add_actor', json={"actor_id": 1}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #Delete actor from movie
        res = self.client().patch('/movies/1/delete_actor', json={"actor_id": 1}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #Delete the movie
        res = self.client().delete('/movies/1', headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #Delete the actor
        res = self.client().delete('/actors/1', headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_422_if_add_actor_to_nonexistent_movie_on_patch(self):
        res = self.client().patch('/movies/100/add_actor', json={"actor_id": 1}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)

    def test_422_if_delete_actor_from_nonexistent_movie(self):
        res = self.client().patch('/movies/100/delete_actor', json={"actor_id": 1}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)



    #CASTING ASSISTANT TESTS
    def test_post_by_casting_assistant(self):
        res = self.client().post('/movies', json={"title": "Top Gun", "release_date": "1986-05-16"}, headers={"Authorization": "Bearer {}".format(self.casting_asst_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_by_casting_assistant(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(self.casting_asst_jwt)})
        data = json.loads(res.data)
        self.assertEqual(len(data['movies']), 0)


    #CASTING DIRECTOR TESTS     
    def test_post_by_casting_director(self):
        res = self.client().post('/movies', json={"title": "Top Gun", "release_date": "1986-05-16"}, headers={"Authorization": "Bearer {}".format(self.casting_dir_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_by_casting_director(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(self.casting_dir_jwt)})
        data = json.loads(res.data)
        self.assertEqual(len(data['movies']), 0)

   
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
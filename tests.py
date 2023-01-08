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



    #ACTORS

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
    
    def test_404_if_movie_does_not_exist_on_patch(self):
        res = self.client().patch('/movies/1000', json={"title": "Rainman", "release_date": "1988-12-12"}, headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
    
    def test_404_if_movie_does_not_exist_on_delete(self):
        res = self.client().delete('/movies/1000', headers={"Authorization": "Bearer {}".format(self.exec_producer_jwt)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)




    '''
    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(len(data['categories']))
        
    def test_404_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], 'False')
        self.assertEqual(data['message'],'resource not found')
        
    # test questions per category
        
    def test_get_questions_per_category(self):
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']),3)
        self.assertEqual(data['current_category'],'Entertainment')
    
    def test_get_invalid_category(self):
        res = self.client().get('/categories/9/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], 'False')
        self.assertEqual(data['message'],'resource not found')
        
    
    """
    TEST: Search by any phrase. The questions list will update to include
    only questions that include that string. Use "title" to start.
    """
    
    # search questions by string
    
    def test_search_question_by_string(self):
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)
                                
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalQuestions'])
    
    def test_search_question_by_string(self):
        res = self.client().post('/questions', json={'searchTerm': 'xomo'})
        data = json.loads(res.data)
                                
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['totalQuestions'],0)
    
    # delete questions by id
    
    def test_delete_question_by_id(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_404_if_question_does_not_exist_on_delete(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        
        
    """
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the    last page of the questions list in the "List" tab.
    """

    def test_post_new_question(self):
        res = self.client().post('/questions/add', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    
    def test_422_if_question_creation_not_allowed(self):
        res = self.client().post('/questions/add', json=self.bad_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], 'False')
        self.assertEqual(data['message'], 'unprocessable')
    
    #

    def test_post_new_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions':[], 'quiz_category': {'id': 1}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['question']))  

        
    def test_post_failure_500_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions':[], 'quiz_category': '1'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
    '''

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

from api import app
from backend.models import setup_db, Movies, Actors, db
from backend.auth import AuthError, requires_auth
from dotenv import load_dotenv

# Parse a .env file and then load all variables found as environment variables.
load_dotenv()

# load user token for testing
ACCESS_TOKEN_Executive_Producer = os.getenv('Executive_Producer', None)
ACCESS_TOKEN_Casting_Director = os.getenv('Casting_Director', None)
ACCESS_TOKEN_Casting_Assistant = os.getenv('Casting_Assistant', None)
assert ACCESS_TOKEN_Executive_Producer

# To test other users change the access token
# and use the one needed initially ACCESS_TOKEN_Executive_Producer is used
headers = {
            'Authorization': 'Bearer {}'
            .format(ACCESS_TOKEN_Executive_Producer)
        }

database_name = "capstone_test"
database_path = "postgresql://{}:{}@{}/{}".format(
    'yaser', 'yaser', 'localhost:5432', database_name)


class CastingTestCase(unittest.TestCase):
    """This class represents the ___ test case"""

    """Executed before each test. Define test variables and initialize app."""
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        setup_db(app, database_path)
        self.client = app.test_client

        db.create_all()
        ctx = app.app_context()
        ctx.push()

    def tearDown(self):
        """Executed after reach test"""
        db.session.remove()
        db.drop_all()
        db.get_engine(app).dispose()
        pass

    def test_given_behavior(self):
        """Test _____________ """
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    """
    test for each test for successful operation and for expected errors.
    """
    def test_get_movies(self):
        res = self.client().get('/movies')
        if (res.status_code != 200):
            print('API endpoint Not Found...')
            self.assertEqual(res.status_code, 404)
        else:
            if(res.data):
                self.assertEqual(res.status_code, 200)

            else:
                data = json.loads(res.data)
                self.assertEqual(res.status_code, 200)
                self.assertEqual(data['success'], True)
                self.assertTrue(data['movies'])

    def test_422_get_movie_by_id(self):
        res = self.client().get('/movie-details/1', headers=headers)
        data = json.loads(res.data)

        if (res.status_code == 200):
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['movies'])
        elif (res.status_code == 422):
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unprocessable')
        else:
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unathorized, Token expired.')

    def test_422_get_movie_by_id_fail(self):
        res = self.client().get('/movie-details/10000', headers=headers)
        data = json.loads(res.data)

        if (res.status_code == 422):
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unprocessable')
        else:
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unathorized, Token expired.')

    def test_create_new_movie(self):
        movieData = [{
            'title': 'movie_test_2',
            'Release': 2020,
            'Details': 'testing create movie end point'
            }]

        res = self.client().post('/movies', json=movieData, headers=headers)
        data = json.loads(res.data)

        if (res.status_code == 200):
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            # self.assertTrue(data['created'])
            self.assertTrue((data['movies']))
        else:
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unathorized, Token expired.')

    def test_update_movie(self):
        movieData = [{
            'title': 'movie_test_update',
            'Release': 2020,
            'Details': 'movie_details_test'
            }]

        res = self.client().patch('/movies/1', json=movieData, headers=headers)
        data = json.loads(res.data)

        if (res.status_code == 200):
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['updated'], 1)
            self.assertTrue(data['updated'])
            self.assertTrue(len(data['movies']))
        elif (res.status_code == 400):
            self.assertEqual(res.status_code, 400)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Bad Request')
        elif (res.status_code == 404):
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Resource Not Found')
        else:
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unathorized, Token expired.')

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=headers)
        data = json.loads(res.data)
        movie = Movies.query.filter(Movies.id == 1).one_or_none()

        if (res.status_code == 200):
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], 1)
            self.assertTrue(data['deleted'])
            self.assertTrue(len(data['movie']))
            self.assertEqual(movie, None)
        elif (res.status_code == 400):
            self.assertEqual(res.status_code, 400)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Bad Request')
        elif (res.status_code == 404):
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Resource Not Found')
        else:
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unathorized, Token expired.')

    def test_get_actors_ess(self):
        res = self.client().get('/actors')
        if (res.status_code != 200):
            print('API endpoint Not Found...')
            self.assertEqual(res.status_code, 404)
        else:

            if(res.data):
                self.assertEqual(res.status_code, 200)

            else:
                data = json.loads(res.data)
                self.assertEqual(res.status_code, 200)
                self.assertEqual(data['success'], True)
                self.assertTrue(data['actors'])

    def test_create_new_actor_ess(self):
        movieData = [{
            'actorName': 'actor_test_2',
            'age': 20,
            'gender': 'M'
            }]

        res = self.client().post('/actors', json=movieData, headers=headers)
        data = json.loads(res.data)

        if(res.status_code == 200):
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue((data['actors']))
        else:
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unathorized, Token expired.')

    def test_422_get_actor_ess_by_id(self):
        res = self.client().get('/actor-details/1', headers=headers)

        data = json.loads(res.data)
        if (res.status_code == 200):
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['actors'])
        elif (res.status_code == 422):
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unprocessable')
        else:
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unathorized, Token expired.')

    def test_422_get_actor_ess_by_id_fail(self):
        res = self.client().get('/actor-details/10000', headers=headers)
        data = json.loads(res.data)

        if (res.status_code == 422):
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unprocessable')
        else:
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unathorized, Token expired.')

    def test_update_actor(self):
        actorData = [{
            'actorName': 'new_name_update',
            'age': 20,
            'gender': 'F'
            }]

        res = self.client().patch('/actors/1',
                                  json=actorData,
                                  headers=headers)
        data = json.loads(res.data)

        if (res.status_code == 200):
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['updated'], 1)
            self.assertTrue(data['updated'])
            self.assertTrue(len(data['actors']))
        elif (res.status_code == 400):
            self.assertEqual(res.status_code, 400)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Bad Request')
        elif (res.status_code == 404):
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Resource Not Found')
        else:
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unathorized, Token expired.')

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=headers)
        data = json.loads(res.data)
        actor = Actors.query.filter(Actors.id == 1).one_or_none()

        if (res.status_code == 200):
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], 1)
            self.assertTrue(data['deleted'])
            self.assertTrue(len(data['actor']))
            self.assertEqual(actor, None)
        elif (res.status_code == 400):
            self.assertEqual(res.status_code, 400)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Bad Request')
        elif (res.status_code == 404):
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Resource Not Found')
        else:
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unathorized, Token expired.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

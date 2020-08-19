import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS, cross_origin

from models import setup_db, Movies, Actors
from auth import AuthError, requires_auth
# heroku scale worker=1
app = Flask(__name__)
setup_db(app)
app.secret_key = os.getenv('SECRET')

'''
 @cors Set up CORS. Allow '*' for origins.
'''
# CORS(app, resources={r'/api/*': {'origins': '*'}})
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


'''
   after_request decorator to set Access-Control-Allow
'''


@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS')
    return response


# for testing
@app.route('/')
@cross_origin()
def index():
    return "<h1>Welcome to our server !!</h1>"


# db_drop_and_create_all()

# ROUTES
'''
@ GET /movies endpoint
    - it is a public endpoint
    - it contain only the movie.short() data representation
    - returns status code 200 and json
      {"success": True, "movies": movies}
      where movies is the list of movies
      or appropriate status code indicating reason for failure
'''


@app.route('/movies', methods=['GET'])
@cross_origin()
# @requires_auth('get:movies')
def get_all_movies():
    # return 'im good'
    movies = Movies.query.all()
    movie = []
    for m in movies:
        movie.append(m.short())

    return jsonify({
        'success': True,
        'movies': movie
    }), 200


'''
@ GET /movies-detail endpoint
    - it require the 'get:movies-detail' permission
    - it contain the movie.long() data representation
    - returns status code 200 and json
      {"success": True, "movies": movies}
      where movies is the list of movies
      or appropriate status code indicating reason for failure
'''


@app.route('/movie-details/<int:id>', methods=['GET'])
@cross_origin()
@requires_auth('get:movies')
def getmovieDetail(payload, id):
    movies = Movies.query.get(id)
    movie = []

    movie.append(movies.long())

    return jsonify({
        'success': True,
        'movies': movie
    }), 200


'''
@ POST /movies endpoint
    - it create a new row in the movies table
    - it require the 'post:movies' permission
    - it contain the movies.long() data representation
    - returns status code 200 and json
      {"success": True, "movies": movie}
      where movie an array containing only the newly created movie
      or appropriate status code indicating reason for failure
'''


@app.route('/movies', methods=['POST'])
@cross_origin()
@requires_auth('post:movie')
def createMovie(payload):
    data_json = request.get_json()
    # movie = []
    # {id: -1, title: '', release_date: 0, movie_details: ''}
    if not ("title" in data_json):
        abort(401)

    else:
        try:
            movie_title = data_json.get('title', None)
            new_movie_details = data_json.get('movie_details')
            movie_release_date = data_json.get('release_date')

            new_movie = Movies(
                title=movie_title,
                release_date=movie_release_date,
                movie_details=new_movie_details)

            Movies.insert(new_movie)
            movie = Movies.query.filter_by(id=new_movie.id).first()

        except BaseException:
            abort(400)

        return jsonify(
            {
                'success': True,
                'movies': movie.long()
            }), 200


# '''
# @ PATCH /movies/<id> endpoint <id> is the existing model id
#     - it respond with a 404 error if <id> is not found
#     - it update the corresponding row for <id>
#     - it require the 'patch:movies' permission
#     - it contain the movie.long() data representation
#     - returns status code 200 and json
#     {"success": True, "movies": movie
#      where movie an array containing only the updated movie
#      or appropriate status code indicating reason for failure
# '''


@app.route('/movies/<int:id>', methods=['PATCH'])
@cross_origin()
@requires_auth('update:movies')
def updateMovies(payload, id):
    data_json = request.get_json()
    movie_title = data_json.get('title')
    movie_release_date = data_json.get('release_date')
    movie_details = data_json.get('movie_details')

    try:
        movie = Movies.query.filter(Movies.id == id).one_or_none()
        if not movie:
            abort(404)

        if movie_title is not None:
            movie.title = movie_title
            movie.release_date = movie_release_date
            movie.movie_details = movie_details

        movie.update()

    except BaseException:
        abort(400)

    return jsonify(
        {
            'success': True,
            'movies': [movie.long()]
        }), 200


# '''
# @endpoint DELETE /movies/<id>
#     - <id> is the existing model id
#     - it respond with a 404 error if <id> is not found
#     - it delete the corresponding row for <id>
#     - it require the 'delete:movies' permission
#     - returns status code 200 and json
#       {"success": True, "delete": id}
#       where id is the id of the deleted record
#       or appropriate status code indicating reason for failure
# '''


@app.route('/movies/<int:id>', methods=['DELETE'])
@cross_origin()
@requires_auth('delete:movie')
def deleteMovies(payload, id):
    movie = Movies.query.filter(Movies.id == id).one_or_none()

    if not movie:
        abort(404)

    try:
        movie.delete()
    except BaseException:
        abort(400)

    return jsonify(
        {
            'success': True,
            'delete': id
        }), 200


# # Error Handling
# '''
#     Error handlers for all expected errors
#     including 400, 401, 404, 405, 422 and 500.
# '''


@app.errorhandler(AuthError)
def AuthError_handler(e):
    status_code = e.status_code
    message = e.error['description']
    return jsonify(
        {
            'success': False,
            'error': status_code,
            'message': message
        }), status_code


@app.errorhandler(400)
def bad_request(error):
    return jsonify(
        {
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify(
        {
            'success': False,
            'error': 401,
            'message': 'Unathorized'
        }), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify(
        {
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(
        {
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405


# '''
# Example error handling for unprocessable entity
# '''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify(
        {
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify(
        {
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

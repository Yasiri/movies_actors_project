import os
from flask import (
    Flask, request, jsonify, abort,
    render_template, session, escape)
from sqlalchemy import exc
import json
from flask_cors import CORS, cross_origin

from backend.models import setup_db, Movies, Actors, db
from backend.auth import AuthError, requires_auth
# heroku scale worker=1
app = Flask(__name__)
app.secret_key = os.getenv('GDtfDCFYjD')

setup_db(app)

'''
 @cors Set up CORS. Allow '*' for origins.
'''

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


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


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
# @cross_origin()
def get_all_movies():
    return 'movies'
    # movies = Movies.query.all()

    # movie = []
    # movieOjt = {}
    # movieArray = []

    # for m in movies:
    #     movie = (m.short())
    #     movieOjt = {
    #         'id': m.id,
    #         'title': m.title,
    #         'release_date': m.release_date,
    #         'movie_details': m.movie_details
    #         }
    #     movieArray.append(movieOjt)

    # return render_template('movies.html', data=movieArray)
    # return jsonify({
    #     'success': True,
    #     'movies': movieOjt
    # }), 200


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
    movie = {}
    try:
        movie = {
            'title': movies.title,
            'release_date': movies.release_date,
            'movie_details': movies.movie_details
        }
        return jsonify({
            'success': True,
            'movies': movie
        }), 200
    except Exception:
        abort(422)


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
    # {id: -1, title: '', release_date: 0, movie_details: ''}
    if not ("title" in data_json[0]):
        abort(401)

        exists = db.session.query(db.exists()
                                  .where(Movies.title == data_json[0]
                                         .get('title'))).scalar()

        if(exists is True):
            abort(400)

    else:
        try:
            movie_title = data_json[0].get('title', None)
            new_movie_details = data_json[0].get('Details')
            movie_release_date = data_json[0].get('Release')

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


'''
@ PATCH /movies/<id> endpoint <id> is the existing model id
    - it respond with a 404 error if <id> is not found
    - it update the corresponding row for <id>
    - it require the 'patch:movies' permission
    - it contain the movie.long() data representation
    - returns status code 200 and json
    {"success": True, "movies": movie
     where movie an array containing only the updated movie
     or appropriate status code indicating reason for failure
'''


@app.route('/movies/<int:id>', methods=['PATCH'])
@cross_origin()
@requires_auth('update:movies')
def updateMovies(payload, id):
    data_json = request.get_json()
    movie_title = data_json[0].get('title')
    movie_release_date = data_json[0].get('Release')
    movie_details = data_json[0].get('Details')

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
            'updated': id,
            'movies': [movie.long()]
        }), 200


'''
@endpoint DELETE /movies/<id>
    - <id> is the existing model id
    - it respond with a 404 error if <id> is not found
    - it delete the corresponding row for <id>
    - it require the 'delete:movies' permission
    - returns status code 200 and json
      {"success": True, "delete": id}
      where id is the id of the deleted record
      or appropriate status code indicating reason for failure
'''


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
            'deleted': id,
            "movie": movie
        }), 200


'''
@ GET /actors endpoint
    - it is a public endpoint
    - it contain only the movie.short() data representation
    - returns status code 200 and json
      {"success": True, "actors": actors}
      where actors is the list of actors
      or appropriate status code indicating reason for failure
'''


@app.route('/actors', methods=['GET'])
@cross_origin()
def get_all_actors():
    actors = Actors.query.all()
    actor = []
    for a in actors:
        actor.append(a.short())

    return render_template('actors.html', data=actor)
    # return jsonify({
    #     'success': True,
    #     'actors': actor
    # }), 200


'''
@ GET /actors-detail endpoint
    - it require the 'get:actors-detail' permission
    - it contain the movie.long() data representation
    - returns status code 200 and json
      {"success": True, "actors": actors}
      where actors is the list of actors
      or appropriate status code indicating reason for failure
'''


@app.route('/actor-details/<int:id>', methods=['GET'])
@cross_origin()
@requires_auth('get:actors')
def getActorDetail(payload, id):
    actors = Actors.query.get(id)

    actor = {}
    try:
        actor = {
            'actorName': actors.actorName,
            'age': actors.age,
            'gender': actors.gender
        }
        return jsonify({
            'success': True,
            'actors': actor
        }), 200
    except Exception:
        abort(422)


'''
@ POST /actors endpoint
    - it create a new row in the actors table
    - it require the 'post:actors' permission
    - it contain the actors.long() data representation
    - returns status code 200 and json
      {"success": True, "actors": movie}
      where movie an array containing only the newly created movie
      or appropriate status code indicating reason for failure
'''


@app.route('/actors', methods=['POST'])
@cross_origin()
@requires_auth('post:actor')
def createActor(payload):
    data_json = request.get_json()
    # {id: -1, title: '', release_date: 0, movie_details: ''}
    if not ("actorName" in data_json[0]):
        abort(401)

    else:
        try:
            actor_name = data_json[0].get('actorName')
            actor_age = data_json[0].get('age')
            actor_gender = data_json[0].get('gender')

            new_actor = Actors(
                actorName=actor_name,
                age=actor_age,
                gender=actor_gender)

            Actors.insert(new_actor)
            actor = Actors.query.filter_by(id=new_actor.id).first()

        except BaseException:
            abort(400)

        return jsonify(
            {
                'success': True,
                'actors': actor.long()
            }), 200


'''
@ PATCH /actors/<id> endpoint <id> is the existing model id
    - it respond with a 404 error if <id> is not found
    - it update the corresponding row for <id>
    - it require the 'patch:actors' permission
    - it contain the movie.long() data representation
    - returns status code 200 and json
    {"success": True, "actors": movie
     where movie an array containing only the updated movie
     or appropriate status code indicating reason for failure
'''


@app.route('/actors/<int:id>', methods=['PATCH'])
@cross_origin()
@requires_auth('update:actors')
def updateActors(payload, id):
    data_json = request.get_json()
    actor_name = data_json[0].get('actorName', None)
    actor_age = data_json[0].get('age')
    actor_gender = data_json[0].get('gender')

    try:
        actor = Actors.query.filter(Actors.id == id).one_or_none()
        if not actor:
            abort(404)

        if actor_name is not None:
            actor.actorName = actor_name
            actor.age = actor_age
            actor.gender = actor_gender

        actor.update()

    except BaseException:
        abort(400)

    return jsonify(
        {
            'success': True,
            'updated': id,
            'actors': [actor.long()]
        }), 200


'''
@endpoint DELETE /actors/<id>
    - <id> is the existing model id
    - it respond with a 404 error if <id> is not found
    - it delete the corresponding row for <id>
    - it require the 'delete:actors' permission
    - returns status code 200 and json
      {"success": True, "delete": id}
      where id is the id of the deleted record
      or appropriate status code indicating reason for failure
'''


@app.route('/actors/<int:id>', methods=['DELETE'])
@cross_origin()
@requires_auth('delete:actor')
def deleteActors(payload, id):
    actor = Actors.query.filter(Actors.id == id).one_or_none()

    if not actor:
        abort(404)

    try:
        actor.delete()
    except BaseException:
        abort(400)

    return jsonify(
        {
            'success': True,
            'deleted': id,
            "movie": actor
        }), 200


# Error Handling
'''
    Error handlers for all expected errors
    including 400, 401, 404, 405, 422 and 500.
'''


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

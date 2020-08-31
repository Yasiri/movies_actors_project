# Casting Agency

The Casting Agency system models a company that is responsible for creating movies and managing and assigning actors to those movies to simplify and streamline its process.

Hosted on heroku. [Link](https://fsnd-movie-project.herokuapp.com/).

## Motivation

To complete my udacity FSND nanodegree to graduate as this capstone project is my final task.

#### Virtual Enviornment

it is  recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

## Dependencies

Once you have your virtual environment setup and running, install dependencies in the `requirements.txt` file  by running the following command:

```bash
`pip install -r requirements.txt`
```

This will install all of the required packages selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `movies_actors_project` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

OR
AUTOMATICALLY LOAD ENVIRONMENT VARIABLES IN FLASK `.flaskenv`  by running:

```bash
pip install python-dotenv
```

then run: 

```bash
flask run
```

## Authentication

The Auth0 domain and api audience are:
Auth0 domain: `https://fsndy.auth0.com`
api audience: `CapstonApi`

<!-- There are 3 users for this API:

1. Executive Producer

```
email: ExecutiveProducer@FSND.com
password: Ep@fsnd123
```

2. Casting Director 

```
email: CastingDirector@FSND.com
password: Ep@fsnd123
```

3. Casting Assistant 

```
email: CastingAssistant@FSND.com
password: Ep@fsnd123
``` -->

## Endpoints

### `GET /movies`

Retrieves all movies from the Capstone Database.

Response:

```json5
{
  "movies": [
    {
      "id": 1,
      "movie_details": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
      "release_date": "1994",
      "title": "The Shawshank Redemption"
    },
    {
      "id": 2,
      "movie_details": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
      "release_date": "1972",
      "title": "The Godfather"
    }
  ],
  "success": true
}
```

### `POST /movies`

Adds a new movie to the db.

Data:

```json5
[
    {
        "title": "12 Angry Men",
        "release_date": "1957-08-14",
        "movie_details": "A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence."
    }
]
```

Response:

```json5
{
  "movies": {
    "id": 24,
    "movie_details": "A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence.",
    "release_date": "1957",
    "title": "12 Angry Men"
  },
  "success": true
}
```

### `PATCH /movies/<int:id>`

Edit data on a movie in the db.

Data:

```json5
[
    {
        "title": "12 Angry Men 2",
        "release_date": "1957-08-14",
        "movie_details": "A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence."
    }
]
```

Response:

```json5
{
  "movies": [
    {
      "id": 11,
      "movie_details": "A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence.",
      "release_date": "1957",
      "title": "12 Angry Men 2"
    }
  ],
  "success": true,
  "updated": 11
}
```

### `DELETE /movies/<int:id>`

Delete a movie from the db.

Response:

```json5
{
  "deleted": 11,
  "movie": {
    "id": 11,
    "movie_details": "A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence.",
    "release_date": "Wed, 14 Aug 1957 00:00:00 GMT",
    "title": "12 Angry Men 2"
  },
  "success": true
}
```

### `GET /actors`

Gets all actors from the db.

Response:

```json5
{
  "actors": [
    {
      "actorName": " Henry Fonda",
      "age": 77,
      "gender": "M",
      "id": 1
    },
    {
      "actorName": "Al Pacino",
      "age": 60,
      "gender": "M",
      "id": 2
    }
  ],
  "success": true
}
```

### `POST /actors`

Adds a new actor to the db.

Data:

```json5
[
    {
        "actorName": "Tim Robbins",
        "age": 62,
        "gender": "M"
    }
]
```

Response:

```json5
{
  "actors": {
    "actorName": "Tim Robbins",
    "age": 62,
    "gender": "M",
    "id": 3
  },
  "success": true
}
```

### `PATCH /actors/<int:id>`

Edit data on a actor in the db.

Data:

```json5
[
    {
        "actorName": "Tim Robbins",
        "age": 55,
        "gender": "M"
    }
]
```

Response:

```json5
{
  "actors": [
    {
      "actorName": "Tim Robbins",
      "age": 62,
      "gender": "M",
      "id": 3
    }
  ],
  "success": true,
  "updated": 3
}
```

### `DELETE /actors/<int:id>`

Delete a actor from the db.

Response:

```json5
{
  "deleted": 2,
  "movie": {
    "actorName": "Al Pacino",
    "age": 60,
    "gender": "M",
    "id": 2
  },
  "success": true
}
```

## Tests

To run the tests, run `python test.py`.

import json
import requests
from flask import Flask, render_template, make_response
from flask_caching import Cache

app = Flask(__name__, template_folder='templates')

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@app.errorhandler(500)
def internal_error(err):
    return render_template("500.html", err=err), 500

def get_movies(url):

    movies = dict()
    req = requests.get(url)
    if req.status_code != 200:
        # to be logged
        return internal_error(f"error : {url} : {req.status_code}")
    json_movie = json.loads(req.content.decode('utf-8'))
    for record in json_movie:
        movies["https://ghibliapi.herokuapp.com/films/" + record["id"]] = (record["title"], [])
    return get_people("https://ghibliapi.herokuapp.com/people?limit=250", movies=movies)

def get_people(url, movies=None):

    req = requests.get(url)
    if req.status_code != 200:
        # to be logged
        return internal_error(f"error : {url} : {req.status_code}")
    json_people = json.loads(req.content.decode('utf-8'))
    for record in json_people:
        for movie in record['films']:
            if movie not in movies.keys():
                movies[movie][1] = [record['name']]
            else:
                movies[movie][1].append(record['name'])

    return render_template('movies.html', movies=movies), 200


@app.route('/<page_name>')
def other(page_name):
    response = make_response('The page named %s does not exist.' \
                             % page_name, 404)
    return response

@app.route('/movies')
@cache.cached(timeout=60)
def ghibli_person_display():

    return get_movies("https://ghibliapi.herokuapp.com/films?limit=250")

import os

from flask import Flask, render_template, jsonify, redirect, request, abort
from flask_cors import CORS

from models import setup_db, db, Movies, Actors
from auth import requires_auth, AuthError, get_login_url, get_logout_url


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # @app.route('/')
    # def get_greeting():
    #     excited = os.environ['EXCITED']
    #     greeting = "Hello"
    #     if excited == 'true':
    #         greeting = greeting + "!!!!! You are doing great in this Udacity project."
    #     return greeting

    # @app.route('/coolkids')
    # def be_cool():
    #     return "Be cool, man, be coooool! You're almost a FSND grad!"

    @app.route('/')
    def home_page():
        return render_template('index.html', 
            title='Casting Agency',
            login_url=get_login_url(),
            logout_url=get_logout_url())


    @app.route('/login_callback')
    def login_callback():
        return render_template('login_callback.html',
            title='Login processing')


    @app.route('/logout_callback')
    def logout_callback():
        return render_template('logout_callback.html',
            title='Logout processing')


    @app.route('/api/movies', methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_movies(payload):
        movies = Movies.query.order_by('id').all()
        return jsonify({
            'success': True,
            'count': len(movies),
            'movies': [movie.format() for movie in movies]
        })


    @app.route('/api/movies/<int:id>', methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_a_movie_detail(payload, id):
        movie = Movies.query.get(id)
        if movie is None:
            abort(404)
        
        return jsonify({
            'success': True,
            'movie': movie.format(),
            'actors': movie.format_actors(),
        })


    @app.route('/api/movies', methods=['POST'])
    @requires_auth(permission='post:movies')
    def post_a_movie(payload):
        body = request.get_json()
        if body is None:
            abort(422)

        title = body.get('title')
        release_date_string = body.get('release_date')

        if title is None or title == '' or\
            release_date_string is None or release_date_string == '':
            abort(422)

        release_date = None
        try:
            release_date = Movies.date_string_to_object(release_date_string)
        except:
            abort(422)

        movie = Movies(title=title, release_date=release_date)
        movie.insert()

        return jsonify({
            'success': True,
            'movie_id': movie.id,
        })


    @app.route('/api/movies/<int:id>/actors', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def movie_associates_actor(payload, id):
        movie = Movies.query.get(id)
        if movie is None:
            abort(404)

        body = request.get_json()
        if body is None:
            abort(422)

        # the attaching of actor and movie state
        # when its value is true dedicating that the actor associates with the movie
        # otherwise, the actor disconnets the movie
        attach_state = body.get('attach_state')
        if attach_state is None or isinstance(attach_state, bool) == False:
            abort(422)

        actor_id = body.get('actor_id')
        if actor_id is None:
            abort(422)

        actor = Actors.query.get(actor_id)
        if actor is None:
            abort(422)

        if attach_state == True:
            if actor not in movie.actors:
                movie.actors.append(actor)
        else:
            if actor in movie.actors:
                movie.actors.remove(actor)

        movie.update()

        return jsonify({
            'success': True,
        })


    @app.route('/api/movies/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def patch_an_movie(payload, id):
        movie = Movies.query.get(id)
        if movie is None:
            abort(404)

        body = request.get_json()
        if body is None:
            abort(422)
        
        title = body.get('title')
        if title != None:
            if title == '':
                abort(422)
            movie.title = title

        release_date_string = body.get('release_date')
        if release_date_string != None and release_date_string != '':
            try:
                movie.release_date = Movies\
                    .date_string_to_object(release_date_string)
            except:
                abort(422)

        movie.update()

        return jsonify({
            'success': True,
        })


    @app.route('/api/movies/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_a_movie(payload, id):
        movie = Movies.query.get(id)
        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
        })


    @app.route('/api/actors', methods=['GET'])
    @requires_auth(permission='get:actors')
    def get_actors(payload):
        actors = Actors.query.order_by('id').all()
        return jsonify({
            'success': True,
            'count': len(actors),
            'actors': [actor.format() for actor in actors],
        })


    @app.route('/api/actors/<int:id>', methods=['GET'])
    @requires_auth(permission='get:actors')
    def get_an_actor_detail(payload, id):
        actor = Actors.query.get(id)
        if actor is None:
            abort(404)
        
        return jsonify({
            'success': True,
            'actor': actor.format(),
            'movies': actor.format_movies(),
        })


    @app.route('/api/actors', methods=['POST'])
    @requires_auth(permission='post:actors')
    def post_an_actor(payload):
        body = request.get_json()
        if body is None:
            abort(422)
        
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if name is None or name == '' or\
            age is None or isinstance(age, int) == False or\
            gender is None or isinstance(gender, bool) == False:
            abort(422)

        actor = Actors(name=name, age=age, gender=gender)
        actor.insert()

        return jsonify({
            'success': True,
            'actor_id': actor.id,
        })


    @app.route('/api/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
    def patch_an_actor(payload, id):
        actor = Actors.query.get(id)
        if actor is None:
            abort(404)

        body = request.get_json()
        if body is None:
            abort(422)

        name = body.get('name')
        if name != None:
            if name == '':
                abort(422)
            actor.name = name
        
        age = body.get('age')
        if age != None:
            if isinstance(age, int) == False:
                abort(422)
            actor.age = age

        gender = body.get('gender')
        if gender != None:
            if isinstance(gender, bool) == False:
                abort(422)
            actor.gender = gender

        actor.update()

        return jsonify({
            'success': True,
        })


    @app.route('/api/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_an_actor(payload, id):
        actor = Actors.query.get(id)
        if actor is None:
            abort(404)
        
        actor.delete()
        
        return jsonify({
            'success': True,
        })


    @app.errorhandler(404)
    def not_found(err):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found',
        }), 404


    @app.errorhandler(422)
    def unprocessable_entity(err):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity',
        }), 422


    @app.errorhandler(405)
    def method_not_allowed(err):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed',
        }), 405


    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code


    @app.errorhandler(500)
    def method_not_allowed(err):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Please try again later',
        }), 500


    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=8080)

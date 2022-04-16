import os

from flask import Flask, render_template, jsonify, redirect, request, abort
from flask_cors import CORS

from models import setup_db, db, Movies, Actors
from utils import ReleaseDate


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
        return render_template('index.html', title='Casting Agency')


    @app.route('/api/movies', methods=['GET'])
    def get_movies():
        movies = db.session.query(Movies).all()
        return jsonify({
            'success': True,
            'count': len(movies),
            'movies': [movie.format() for movie in movies]
        })


    @app.route('/api/movies/<int:id>', methods=['GET'])
    def get_a_movie_detail(id):
        movie = db.session.query(Movies).get(id)
        if movie is None:
            abort(404)
        
        return jsonify({
            'success': True,
            'movie': movie.format(),
            'actors': [actor.format() for actor in movie.actors],
        })


    @app.route('/api/movies', methods=['POST'])
    def post_a_movie():
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
            release_date = ReleaseDate\
                .date_string_to_object(release_date_string)
        except:
            abort(422)

        movie = Movies(title=title, release_date=release_date)
        movie_id = None
        
        try:
            db.session.add(movie)
            db.session.commit()
        except:
            db.session.rollback()
            abort(500)
        finally:
            movie_id = movie.id
            db.session.close()

        return jsonify({
            'success': True,
            'movie_id': movie_id,
        })


    @app.route('/api/movies/<int:id>/actors', methods=['POST'])
    def movie_associates_actor(id):
        movie = db.session.query(Movies).get(id)
        if movie is None:
            abort(404)

        body = request.get_json()
        if body is None:
            abort(422)

        actor_id = body.get('actor_id')
        if actor_id is None:
            abort(422)

        actor = db.session.query(Actors).get(actor_id)
        if actor is None:
            abort(422)

        try:
            movie.actors.append(actor)
            db.session.commit()
        except:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

        return jsonify({
            'success': True,
        })


    @app.route('/api/movies/<int:id>', methods=['PATCH'])
    def patch_an_movie(id):
        movie = db.session.query(Movies).get(id)
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
                movie.release_date = ReleaseDate\
                    .date_string_to_object(release_date_string)
            except:
                abort(422)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

        return jsonify({
            'success': True,
        })


    @app.route('/api/movies/<int:id>', methods=['DELETE'])
    def delete_a_movie(id):
        movie = db.session.query(Movies).get(id)
        if movie is None:
            abort(404)

        try:
            db.session.delete(movie)
            db.session.commit()
        except:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

        return jsonify({
            'success': True,
        })


    @app.route('/api/actors', methods=['GET'])
    def get_actors():
        actors = db.session.query(Actors).all()
        return jsonify({
            'success': True,
            'count': len(actors),
            'actors': [actor.format() for actor in actors],
        })


    @app.route('/api/actors/<int:id>', methods=['GET'])
    def get_an_actor_detail(id):
        actor = db.session.query(Actors).get(id)
        if actor is None:
            abort(404)
        
        return jsonify({
            'success': True,
            'actor': actor.format(),
            'movies': [movie.format() for movie in actor.movies],
        })


    @app.route('/api/actors', methods=['POST'])
    def post_an_actor():
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
        actor_id = None
        
        try:
            db.session.add(actor)
            db.session.commit()
        except:
            db.session.rollback()
            abort(500)
        finally:
            actor_id = actor.id
            db.session.close()

        return jsonify({
            'success': True,
            'actor_id': actor_id,
        })


    @app.route('/api/actors/<int:id>', methods=['PATCH'])
    def patch_an_actor(id):
        actor = db.session.query(Actors).get(id)
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

        try:
            db.session.commit()
        except:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

        return jsonify({
            'success': True,
        })


    @app.route('/api/actors/<int:id>', methods=['DELETE'])
    def delete_an_actor(id):
        actor = db.session.query(Actors).get(id)
        if actor is None:
            abort(404)
        
        try:
            db.session.delete(actor)
            db.session.commit()
        except:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()
        
        return jsonify({
            'sucess': True,
        })


    # @app.route('/login')
    # def login():
    #     pass

    # @app.route('/logout')
    # def logout():
    #     pass


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

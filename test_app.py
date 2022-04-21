import os
import json
import unittest
from wsgiref import headers

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Movies, Actors


'''
Prepare the token belong with three roles for next testing.
'''
token_file = open('./test_token.json')
tokens = json.load(token_file)
token_file.close()


'''
Record the generated models' id for next cases.
'''
ready_movie_id = None
ready_actor_id = None
not_exist_id = 0


class CastingAgencyTestCase(unittest.TestCase):


	def setUp(self):
		self.database_url = os.environ['TEST_DATABASE_URL']
		self.app = create_app({
			'database_url': self.database_url
		})
		self.client = self.app.test_client

		with self.app.app_context():
			self.db = SQLAlchemy()
			self.db.init_app(self.app)
			self.db.create_all()


	def tearDown(self):
		pass


	def create_token(self, role):
		return 'Bearer {}'.format(tokens.get(role))


	def test_01_post_movies_success(self):
		res = self.client().post('/api/movies', headers={
			'Authorization': self.create_token('producer')
		}, json={
			'title': 'test post movie',
			'release_date': '2022-04-30'
		})
		body = json.loads(res.data)
		
		global ready_movie_id
		ready_movie_id = body['movie_id']

		self.assertEqual(body['success'], True)


	def test_02_post_movies_failed(self):
		res = self.client().post('/api/movies', headers={
			'Authorization': self.create_token('producer')
		}, json={
			'title': 'test post movie'
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], False)
		self.assertEqual(body['error'], 422)


	def test_03_post_actors_success(self):
		res = self.client().post('/api/actors', headers={
			'Authorization': self.create_token('producer')
		}, json={
			'name': 'test post actor',
			'age': 30,
			'gender': False
		})
		body = json.loads(res.data)

		global ready_actor_id
		ready_actor_id = body['actor_id']

		self.assertEqual(body['success'], True)


	def test_04_post_actors_failed(self):
		res = self.client().post('/api/actors', headers={
			'Authorization': self.create_token('producer')
		}, json={
			'name': 'test post actor'
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], False)
		self.assertEqual(body['error'], 422)


	def test_05_patch_movies_success(self):
		target_id = ready_movie_id
		res = self.client().patch(f'/api/movies/{target_id}', headers={
			'Authorization': self.create_token('producer')
		}, json={
			'title': 'test post actor patch'
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], True)


	def test_06_patch_movies_failed(self):
		target_id = ready_movie_id
		res = self.client().patch(f'/api/movies/{target_id}', headers={
			'Authorization': self.create_token('producer')
		}, json={
			'title': ''
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], False)
		self.assertEqual(body['error'], 422)


	def test_07_patch_actors_success(self):
		target_id = ready_actor_id
		res = self.client().patch(f'/api/actors/{target_id}', headers={
			'Authorization': self.create_token('producer')
		}, json={
			'name': 'test post actor patch'
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], True)


	def test_08_patch_actors_failed(self):
		target_id = ready_actor_id
		res = self.client().patch(f'/api/actors/{target_id}', headers={
			'Authorization': self.create_token('producer')
		}, json={
			'name': ''
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], False)
		self.assertEqual(body['error'], 422)


	def test_09_assocate_movie_actor_success(self):
		movie_id = ready_movie_id
		res = self.client().patch(f'/api/movies/{movie_id}/actors', headers={
			'Authorization': self.create_token('producer')
		}, json={
			'actor_id': ready_actor_id,
			'attach_state': True
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], True)
		

	def test_10_assocate_movie_actor_failed(self):
		movie_id = ready_movie_id
		res = self.client().patch(f'/api/movies/{movie_id}/actors', headers={
			'Authorization': self.create_token('producer')
		}, json={
			'actor_id': ready_actor_id,
			'attach_state': 0
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], False)
		self.assertEqual(body['error'], 422)


	def test_11_get_movies_success(self):
		res = self.client().get('/api/movies', headers={
			'Authorization': self.create_token('producer')
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], True)
		self.assertEqual(len(body['movies']), body['count'])


	def test_12_get_movies_failed(self):
		res = self.client().get('/api/movies', headers={
			'Authorization': ''
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], False)
		self.assertEqual(body['error'], 401)


	def test_13_get_movies_detail_success(self):
		target_id = ready_movie_id
		res = self.client().get(f'/api/movies/{target_id}', headers={
			'Authorization': self.create_token('producer')
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], True)
		self.assertEqual(body['movie']['id'], target_id)


	def test_14_get_movies_detail_failed(self):
		target_id = not_exist_id
		res = self.client().get(f'/api/movies/{target_id}', headers={
			'Authorization': self.create_token('producer')
		})
		body = json.loads(res.data)

		self.assertEqual(body['error'], 404)


	def test_15_get_actors_success(self):
		res = self.client().get('/api/actors', headers={
			'Authorization': self.create_token('producer')
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], True)
		self.assertEqual(len(body['actors']), body['count'])


	def test_16_get_actors_failed(self):
		res = self.client().get('/api/actors', headers={
			'Authorization': ''
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], False)
		self.assertEqual(body['error'], 401)


	def test_17_get_actors_detail_success(self):
		target_id = ready_actor_id
		res = self.client().get(f'/api/actors/{target_id}', headers={
			'Authorization': self.create_token('producer')
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], True)
		self.assertEqual(body['actor']['id'], target_id)


	def test_18_get_actors_detail_failed(self):
		target_id = not_exist_id
		res = self.client().get(f'/api/actors/{target_id}', headers={
			'Authorization': self.create_token('producer')
		})
		body = json.loads(res.data)

		self.assertEqual(body['error'], 404)


	def test_19_delete_actor_success(self):
		target_id = ready_actor_id
		res = self.client().delete(f'/api/actors/{target_id}', headers={
			'Authorization': self.create_token('producer')
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], True)

	
	def test_20_delete_actor_failed(self):
		target_id = ready_actor_id
		res = self.client().delete(f'/api/actors/{target_id}', headers={
			'Authorization': self.create_token('producer')
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], False)
		self.assertEqual(body['error'], 404)


	def test_21_delete_movie_success(self):
		target_id = ready_movie_id
		res = self.client().delete(f'/api/movies/{target_id}', headers={
			'Authorization': self.create_token('producer')
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], True)

	
	def test_22_delete_movie_failed(self):
		target_id = ready_movie_id
		res = self.client().delete(f'/api/movies/{target_id}', headers={
			'Authorization': self.create_token('producer')
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], False)
		self.assertEqual(body['error'], 404)


	def test_23_producer_post_movie(self):
		res = self.client().post('/api/movies', headers={
			'Authorization': self.create_token('producer')
		}, json={
			'title': 'test post movie with producer role',
			'release_date': '2022-04-30'
		})
		body = json.loads(res.data)
		
		global ready_movie_id
		ready_movie_id = body['movie_id']

		self.assertEqual(body['success'], True)


	def test_24_producer_post_actor(self):
		res = self.client().post('/api/actors', headers={
			'Authorization': self.create_token('producer')
		}, json={
			'name': 'producer',
			'age': 35,
			'gender': False
		})
		body = json.loads(res.data)
		
		global ready_actor_id
		ready_actor_id = body['actor_id']

		self.assertEqual(body['success'], True)


	def test_25_director_delete_movie(self):
		target_id = ready_movie_id
		res = self.client().delete(f'/api/movies/{target_id}', headers={
			'Authorization': self.create_token('director')
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], False)
		self.assertEqual(body['error'], 403)

	
	def test_26_director_delete_actor(self):
		target_id = ready_actor_id
		res = self.client().delete(f'/api/actors/{target_id}', headers={
			'Authorization': self.create_token('director')
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], True)
		

	def test_27_assistant_delete_movie(self):
		target_id = ready_movie_id
		res = self.client().delete(f'/api/movies/{target_id}', headers={
			'Authorization': self.create_token('assistant')
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], False)
		self.assertEqual(body['error'], 403)


	def test_28_assistant_delete_actor(self):
		target_id = ready_actor_id
		res = self.client().delete(f'/api/actors/{target_id}', headers={
			'Authorization': self.create_token('assistant')
		})
		body = json.loads(res.data)

		self.assertEqual(body['success'], False)
		self.assertEqual(body['error'], 403)


if __name__ == '__main__':
	unittest.main()


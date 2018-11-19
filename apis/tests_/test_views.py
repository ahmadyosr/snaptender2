from django.test import TestCase
from django.urls import reverse
import random 
import json
from rest_framework import status
from django.contrib.auth.models import User
from catalogue.models import Snippet

class RegisterAndLoginApiTestCase(TestCase):
	"""Login api 
	"""

	def setUp(self):
		self.username = 'ahmad%d' %(random.random()*10000)
		self.password = 'thisispassword1234'

		self.valid_payload = {
			'username': self.username, 
			'password': self.password,
		}
		self.invalid_payload = {
			'username': '',
			'password':'ahmadyosr'
		}
		self.token = None
		self.user = None

		self.valid_login_payload = {'username':self.username, 
									'password':self.password}

	def test_register(self):
		response = self.client.post(
			reverse('apis:register'),
			data=json.dumps(self.valid_payload),
			content_type='application/json'
		)

		self.token = response.data.get('token')

		self.user = User.objects.get(username= self.username)

		self.assertTrue(len(self.token)>1)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
 
	def test_failed_register(self):
		response = self.client.post(
			reverse('apis:register'),
			data=json.dumps(self.invalid_payload),
			content_type='application/json'
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


	def test_login(self):
		self.test_register()

		response = self.client.post(
			reverse('apis:login'),
			data=json.dumps(self.valid_login_payload),
			content_type='application/json'
		)


		token = response.data['token']

		# change username to change token
		self.user.username='ahmadnewusername'
		self.user.save()

		self.assertFalse(str(self.token) == str(token))
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	# def test_token_authentication(self):
	# 	self.test_register()

	# 	views_names = ['apis:snippets']
	# 	token_payload = {'token':self.token.decode('utf-8')}

	# 	for v in views_names: 

	# 		r = self.client.post(reverse(v),
	# 			data=json.dumps(token_payload),
	# 			content_type='application/json'
	# 			)
	# 		r2 = self.client.post(reverse(v),
	# 			data=json.dumps({}),
	# 			content_type='application/json'
	# 			)

	# 		self.assertEqual(r.status_code ,status.HTTP_201_CREATED)
	# 		self.assertTrue(r2.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_400_BAD_REQUEST))



class SnippetDetailTestCase(RegisterAndLoginApiTestCase):

	def setUp(self):
	        super(SnippetDetailTestCase, self).setUp()
	        self.snippet = Snippet.objects.create()

	def test_snippet_detail(self):
		self.test_register()
		self.snippet_payload = {'token':self.token.decode('utf-8')}

		r = self.client.post(reverse('apis:snippet-detail' , kwargs={'pk':self.snippet.id}),
							json.dumps(self.snippet_payload),
							content_type='application/json'
							)

		snippet_id = r.data.get('id')
		self.assertTrue(snippet_id != None)
		self.assertEqual(r.status_code,status.HTTP_200_OK)

	def test_snippet_detail_without_token(self):
		self.test_register()
		self.snippet_payload = {}

		r = self.client.post(reverse('apis:snippet-detail' , kwargs={'pk':self.snippet.id}),
							json.dumps(self.snippet_payload),
							content_type='application/json'
							)

		self.assertEqual(r.status_code,status.HTTP_401_UNAUTHORIZED)


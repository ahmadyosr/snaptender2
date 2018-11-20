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

		self.token = response.data.get('token').decode('utf-8')

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
		self.snippet_payload = {'token':self.token}

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



class FavoriteTestCase(RegisterAndLoginApiTestCase):

	def setUp(self):
		super(FavoriteTestCase, self).setUp()
		self.favorited = []

	def test_add_favorite(self):
		self.test_register()

		self.url_name = 'apis:snippet-favorite'
		self.favorited = [Snippet.objects.create(is_tender=True, title='this is title %d' %i) for i in range(20)]
		self.snippets = [Snippet.objects.create(is_tender=True, title='this is title %d' %i) for i in range(20)]
		
		prev_user_favs = self.user.userprofile.snippets.all().values('id')
		self.assertTrue(len(prev_user_favs)==0)

		for f in self.favorited:

			self.favorite_payload = {'token':self.token}
			r = self.client.post(reverse(self.url_name , kwargs={'pk':f.id}),
								json.dumps(self.favorite_payload),
								content_type='application/json'
								)


			user_favs = self.user.userprofile.snippets.all()
			self.assertEqual(r.status_code, status.HTTP_200_OK)
			self.assertTrue(f in user_favs) 


	def test_remove_favorite(self):
		self.test_add_favorite()				
		user_snippets = self.user.userprofile.snippets.all()

		for f in user_snippets:
			self.favorite_payload = {'token':self.token}
			r = self.client.post(reverse(self.url_name , kwargs={'pk':f.id}),
								json.dumps(self.favorite_payload),
								content_type='application/json'
								)

			self.assertEqual(r.status_code, status.HTTP_200_OK)

			user_favs = self.user.userprofile.snippets.all()
			self.assertTrue(f not in user_favs) 

	def test_toggle_favorite_without_token(self):
		self.test_add_favorite()
		self.assertTrue(self.user.userprofile.snippets.count() > 0)

		fav_id = self.user.userprofile.snippets.first().id 

		r = self.client.post(reverse(self.url_name , kwargs={'pk':fav_id}),
							json.dumps({}),
							content_type='application/json'
							)
		self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

		

# class FavoritesList(FavoriteTestCase):

# 	def test_user_favs(self):
# 		self.test_add_favorite()
# 		url = reverse('apis:favorites')

# 		r = self.client.post(url,
# 							json.dumps(self.favorite_payload),
# 							content_type='application/json'
# 							)
		
# 		user_snippets_ids = self.user.userprofile.snippets.all()
# 		# print(len(r.data))
# 		print(r.data)

# 		self.assertEqual(r.status_code, status.HTTP_200_OK)


# 		

class TestList(TestCase):

	def test_the_test(self):
		url = reverse('apis:test')

		r = self.client.post(url,
							json.dumps({}),
							content_type='application/json'
							)
		
		print(r.data)
        # print(serializer.data)
        
		self.assertEqual(r.status_code, status.HTTP_200_OK)
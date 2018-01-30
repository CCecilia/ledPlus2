from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
import json

from .models import Agent

c = Client()


class RenderingTests(TestCase):
	c = Client()

	@classmethod
	def setUpTestData(cls):
		user = User.objects.create(
			username='testuser',
			email='testuser@email.com',
			password='password'
		)

		Agent.objects.create(
			user=user,
			company='Test Co'
		)

	def index_view(self):
		response = self.c.get(reverse('webapp:index'))
		# check reponse and template
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'webapp/index.html')

	def dashboard_view(self):
		user = User.objects.get(pk=1)
		self.c.force_login(user)

		response = self.c.get(reverse('webapp:dashboard'))
		# check reponse and template
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'webapp/dashboard.html')

	def dashboard_view_redirect(self):
		response = self.c.get(reverse('webapp:dashboard'))
		# check reponse and template
		self.assertEqual(response.status_code, 302)

	def newsale_view(self):
		user = User.objects.get(pk=1)
		self.c.force_login(user)

		response = self.c.get(reverse('webapp:newSale'))
		# check reponse and template
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'webapp/newSale.html')


class AjaxViewsTests(TestCase):
	c = Client()

	@classmethod
	def setUpTestData(cls):
		user = User.objects.create(
			username='testuser',
			email='testuser@email.com',
			password='password'
		)

		Agent.objects.create(
			user=user,
			company='Test Co'
		)

	def test_ajax_register_success(self):
		# Check register success
		response = self.c.post(reverse('webapp:register'), {
			'register-username': 'testuser1',
			'register-email': 'testuser1@email.com',
			'register-password': 'password',
			'register-company': 'test co'
		})
		self.assertEqual(json.loads(response.content)['status'], 'success')
		self.assertEqual(response.status_code, 200)

	def test_ajax_register_username_in_use(self):
		# Check register failed  username taken
		response = self.c.post(reverse('webapp:register'), {
			'register-username': 'testuser',
			'register-email': 'testuser@email.com',
			'register-password': 'password',
			'register-company': 'test co'
		})
		self.assertEqual(json.loads(response.content)['status'], 'fail')
		self.assertEqual(json.loads(response.content)['error_msg'], 'username already in use')

	def test_ajax_register_email_in_use(self):
		# Check register failed email in use
		response = self.c.post(reverse('webapp:register'), {
			'register-username': 'testuser1',
			'register-email': 'testuser@email.com',
			'register-password': 'password',
			'register-company': 'test co'
		})
		self.assertEqual(json.loads(response.content)['status'], 'fail')
		self.assertEqual(json.loads(response.content)['error_msg'], 'email already in use')

	def test_ajax_register_password_length(self):
		# Check register failed  password length
		response = self.c.post(reverse('webapp:register'), {
			'register-username': 'testuser2',
			'register-email': 'testuser2@email.com',
			'register-password': 'pass',
			'register-company': 'test co'
		})
		self.assertEqual(json.loads(response.content)['status'], 'fail')
		self.assertEqual(json.loads(response.content)['error_msg'], 'password must be atleast 8 characters long')

	def test_ajax_login_fail(self):
		# Check login fail
		response = self.c.post(reverse('webapp:login'), {
			'username': 'testuser5000',
			'password': 'password'
		})
		self.assertEqual(json.loads(response.content)['status'], 'fail')

	def test_ajax_login_success(self):
		# Check login success
		response = self.c.post(reverse('webapp:login'), {
			'username': 'testuser',
			'password': 'password'
		})
		self.assertEqual(response.status_code, 200)

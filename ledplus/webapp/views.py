__author__ = 'christian.cecilia1@gmail.com'
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Agent, Subtype


class HtmlRendering:

	def index(request):
		context = {
			'page': 'index',
		}
		return render(request, 'webapp/index.html', context)

	@login_required
	def dashboard(request):
		user = request.user
		context = {
			'page': 'dashboard',
			'user': user
		}
		return render(request, 'webapp/dashboard.html', context)

	@login_required
	def newSale(request):
		user = request.user
		context = {
			'page': 'new sale',
			'subtypes': Subtype.objects.all().order_by('name')
		}
		return render(request, 'webapp/new-sale.html', context)


class UserViews:

	def register(request):
		# dec vars
		username = str(request.POST['register-username']).lower()
		company = str(request.POST['register-company']).upper()
		email = str(request.POST['register-email']).lower()
		password = str(request.POST['register-password'])

		# check if username or email is used
		username_check = User.objects.filter(username=username)
		email_check = User.objects.filter(email=email)

		if username_check:
			response = {
				'status': 'fail',
				'error_msg': 'username already in use'
			}
			# send reponse JSON
			return JsonResponse(response)
		elif email_check:
			response = {
				'status': 'fail',
				'error_msg': 'email already in use'
			}
			# send reponse JSON
			return JsonResponse(response)
		elif len(password) < 8:
			response = {
				'status': 'fail',
				'error_msg': 'password must be atleast 8 characters long'
			}
			# send reponse JSON
			return JsonResponse(response)
		else:
			# create user
			user = User.objects.create_user(username, email, password)
			# create abstract agent model
			Agent.objects.create(user=user, company=company)

			# login user
			login(request, user)

			response = {
				'status': 'success'
			}
		# send reponse JSON
		return JsonResponse(response)

	def login(request):
		# dec vars
		username = request.POST['username']
		password = request.POST['password']

		# Auth user
		user = authenticate(request, username=username, password=password)

		if not user:
			# create response
			response = {
				'status': 'fail',
				'error_msg': 'username/password incorrect'
			}
		else:
			# login user
			login(request, user)

			response = {
				'status': 'success'
			}

		# send reponse JSON
		return JsonResponse(response)


class SaleViews():

	def create(request):
		response = {
			'status': 'success'
		}
		# send reponse JSON
		return JsonResponse(response)

	def update(request):
		response = {
			'status': 'success'
		}
		# send reponse JSON
		return JsonResponse(response)


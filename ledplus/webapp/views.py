__author__ = 'christian.cecilia1@gmail.com'
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import json
from .models import *


class HtmlRendering:

	def index(request):
		context = {
			'page': 'index',
		}
		return render(request, 'webapp/index.html', context)

	@login_required
	def dashboard(request):
		user = request.user
		if request.user.is_staff:
			sale_count = Sale.objects.all().count()
		else:
			sale_count = Sale.objects.filter(agent=request.user).count()

		context = {
			'page': 'dashboard',
			'user': user,
			'sale_count': sale_count
		}
		return render(request, 'webapp/dashboard.html', context)

	@login_required
	def newSale(request):
		user = request.user
		
		context = {
			'page': 'new sale',
			'subtypes': Subtype.objects.all().order_by('name'),
			'leds': Led.objects.filter(active=True).order_by('order_number'),
			'utilities': Utility.objects.filter(active=True).order_by('name'),
			'service_classes': ServiceClass.objects.filter(active=True).order_by('name'),
		}
		return render(request, 'webapp/new-sale.html', context)

	@login_required
	def sales(request):
		if request.user.is_staff:
			sales = Sale.objects.all()
		else:
			sales = Sale.objects.filter(agent=request.user)

		context = {
			'page': 'sales',
			'sales': sales
		}
		return render(request, 'webapp/sales.html', context)


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

	def logout(request):
		# log out user
		logout(request)

		# send to home page
		return redirect('/')


class SaleViews():

	def addLEDsToSale(sale, leds):
		# clear any existing leds
		[sale.leds.remove(led) for led in sale.leds.all()]

		# create SaleLed obj and associate to sale
		for i in range(len(leds)):
			led = Led.objects.get(id=leds[i]['led_id'])

			# calc wattage reduction
			hoo = int(sale.annual_hours_of_operation)
			wattage_difference = float(led.conventional_wattage) - float(led.wattage)
			# delamp_wattage = leds[i].delamping * float(led.conventional_wattage)
			led_wattage_reduction = wattage_difference * leds[i]['led_count']
			delamp_wattage_reduction = float(led.conventional_wattage) * leds[i]['delamping']
			total_wattage_reduction = led_wattage_reduction + delamp_wattage_reduction
			total_kWh_reduction = (total_wattage_reduction * hoo) / 1000
			
			# js true to python True
			if leds[i]['installation'] == 'true':
				leds[i]['installation'] = True
			else:
				leds[i]['installation'] = False

			sale_led = SaleLed.objects.create(
				led=led,
				color=leds[i]['color'],
				led_count=leds[i]['led_count'],
				total_count=leds[i]['total_lights'],
				not_replacing_count=leds[i]['not_replacing'],
				delamping_count=leds[i]['delamping'],
				wattage_reduction=total_kWh_reduction,
				installation_required=leds[i]['installation'],
				ceiling_height=leds[i]['ceiling_height']
			)
			sale.leds.add(sale_led)

	def update(request):
		# dec vars
		sale_data = json.loads(request.body)

		# check create or update existing
		try:
			sale_id = sale_data['id']
			sale = get_object_or_404(Sale, pk=sale_id)
		except KeyError:
			sale = Sale.objects.create(
				agent=request.user
			)

		# update sale data
		sale.renewal = sale_data['renewal']
		sale.business_name = sale_data['business_name']
		sale.authorized_representative = sale_data['auth_rep']
		sale.service_address = sale_data['service_address']
		sale.service_city = sale_data['service_city']
		sale.service_state = sale_data['service_state']
		sale.service_zip_code = sale_data['service_zip_code']
		subtype = Subtype.objects.get(id=sale_data['subtype'])
		sale.subtype = subtype
		sale.annual_hours_of_operation = sale_data['annual_hours_of_operation']

		# handle leds if present
		try:
			leds = sale_data['leds']
			SaleViews.addLEDsToSale(sale, leds)
		except KeyError:
			pass

		try:
			sale.save()
			response = {
				'status': 'success',
				'sale_id': sale.id
			}
		except Exception as e:
			response = {
				'status': 'fail',
				'error_msg': str(e)
			}

		# send reponse JSON
		return JsonResponse(response)
